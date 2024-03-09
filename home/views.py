from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import DistanceInfo, HospitalImage, Patient, Hospital, Question, Answer, Conclusion, SymptomCheckSession, FavouriteHospital
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import translation
from django.utils.translation import get_language_info, get_language, gettext as _
from datetime import datetime
from django.db.models import Case, When, Value, BooleanField
from django.db.models import Count
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import re



def carePage(request):
    return render(request, 'home/care.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            
        user = authenticate(request, username=username, password=password)   
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
    return render(request, 'account/login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['fullname']and request.POST['gender'] and request.POST['dob'] and request.POST['email']and request.POST['nationality']and request.POST['language']and request.POST['phone']and request.POST['password']and request.POST['repassword'] :
            username =  request.POST['username']
            fullname =  request.POST['fullname']

            gender =  request.POST['gender']
            dob =  request.POST['dob']
            email =  request.POST['email']
            phone =  request.POST['phone']
            nationality =  request.POST['nationality']
            language = request.POST['language']
            password =  request.POST.get('password')
            repassword =  request.POST.get('repassword')
            
            if password == repassword:
              if User.objects.filter(username = username).exists():
                messages.error(request, "Username already taken")
                return redirect('register')

              elif User.objects.filter(email = email).exists():
                messages.error(request,'Email already taken')
                return redirect('register')
              else :
                user = User.objects.create_user(username=username,password=password,email=email)   
                user.save()
                
                patientnew = Patient(user=user,fullname=fullname,dob=dob,gender=gender,email=email,phone=phone,nationality=nationality,language=language)
                patientnew.save()
              return redirect('login')
            else:
                messages.error(request,'Password not matching, please try again')
                return redirect('register') 
            
    return render(request, 'account/signup.html')
            

def home(request):
    request.session['completed'] = False
    request.session['odds_session'] = None
    request.session.pop('conclusion_details', None)
    request.session.modified = True
    if request.user.is_authenticated:
        fullname = request.user.patient.fullname
    else:
        fullname = None
        
    current_time = datetime.now()
    hour = current_time.hour

    if 6 <= hour < 12:
        greeting = _("Good Morning")
    elif 12 <= hour < 18:
        greeting = _("Good Afternoon")
    else:
        greeting = _("Good Evening")
    
    last_session = None
    if request.user.is_authenticated:
        last_session = request.user.symptom_sessions.order_by('-created_at').first()
        if last_session:
            last_session.conclusion_text = _(last_session.conclusion_text)
        
    context = {
        'fullname': fullname,
        'greeting': greeting,
        'last_session': last_session,
    }
    return render(request, 'home/index.html', context)

@login_required
def myData(request):
    fullname = request.user.patient.fullname

    context = {
        'fullname': fullname,
    }

    return render(request, 'account/mydata.html', context)

@login_required
def accountPage(request):
    fullname = request.user.patient.fullname

    context = {
        'fullname': fullname,
    }

    return render(request, 'account/account.html', context)

@login_required
def personalPage(request):
    fullname = request.user.patient.fullname
    gender = request.user.patient.gender
    dob = request.user.patient.dob
    email = request.user.patient.email
    nationality = request.user.patient.nationality
    language = request.user.patient.language

    context = {
        'fullname': fullname,
        'gender': gender,
        'dob': dob,
        'email': email,
        'nationality': _(nationality),
        'language': language,
    }

    return render(request, 'account/personal.html', context)

@login_required
def medicalInfoPage(request):
    fullname = request.user.patient.fullname
    gender = request.user.patient.gender
    dob = request.user.patient.dob
    height = request.user.patient.height
    weight = request.user.patient.weight

    context = {
        'fullname': fullname,
        'gender': gender,
        'dob': dob,
        'height': height,
        'weight': weight,
    }

    return render(request, 'account/medicalInfo.html', context)

@login_required
def setting(request):
    current_language_code = get_language()
    current_language_info = get_language_info(current_language_code)
    
    context = {
        'current_language': _(current_language_info['name']),
    }

    return render(request, 'account/setting.html', context)

@login_required
def passwordsecurityPage(request):
    context = {}

    return render(request, 'account/password&securityPage.html', context)

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePassword')
        else:
            messages.error(request, form.errors)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/changePassword.html', {'form': form})

@login_required
def update_fullname(request):
    page = "fullname"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_fullname = request.POST.get('fullname')
        patient_profile.fullname = new_fullname
        patient_profile.save()
        messages.success(request, 'Your name has been updated.')
        return redirect('personal')
    
    context = {
        'current_fullname': patient_profile.fullname,
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_gender(request):
    page = "gender"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_gender = request.POST.get('gender')
        patient_profile.gender = new_gender
        patient_profile.save()
        messages.success(request, 'Your gender has been updated.')
        return redirect('personal')
    
    context = {
        'current_gender': patient_profile.gender,
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_dob(request):
    page = "dob"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_dob = request.POST.get('dob')
        patient_profile.dob = new_dob
        patient_profile.save()
        messages.success(request, 'Your date of birth has been updated.')
        return redirect('personal')
    
    context = {
        'current_dob': patient_profile.dob.strftime('%Y-%m-%d'), 
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_email(request):
    page = "email"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_email = request.POST.get('email').lower()
        if User.objects.filter(email=new_email).exists():
            messages.error(request, 'Email already exists.')
        else:
            patient_profile.email = new_email
            patient_profile.save()
            request.user.email = new_email 
            request.user.save() 
            messages.success(request, 'Your email has been updated.')
            return redirect('personal')
    
    context = {
        'current_email': patient_profile.email,
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_nationality(request):
    page = "nationality"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_nationality = request.POST.get('nationality')
        patient_profile.nationality = new_nationality
        patient_profile.save()
        messages.success(request, 'Your nationality has been updated.')
        return redirect('personal')
    
    context = {
        'current_nationality': _(patient_profile.nationality), 
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_language(request):
    page = "language"
    patient_profile = request.user.patient
    if request.method == 'POST':
        new_language = request.POST.get('language')
        patient_profile.language = new_language
        patient_profile.save()
        messages.success(request, 'Your language has been updated.')
        return redirect('personal')
    
    context = {
        'current_language': patient_profile.language, 
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_height(request):
    page = "height"
    patient_profile = request.user.patient

    if request.method == 'POST':
        new_height = request.POST.get('height')
        
        try:
            new_height = float(new_height)
            
            if new_height < 0:
                messages.error(request, 'Height cannot be negative.')
                return redirect('medicalInfo')
            
            patient_profile.height = new_height
            patient_profile.save()
            
            messages.success(request, 'Your height has been updated.')
            return redirect('medicalInfo')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid height value. Please enter a valid number.')
    
    context = {
        'current_height': patient_profile.height,
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def update_weight(request):
    page = "weight"
    patient_profile = request.user.patient

    if request.method == 'POST':
        new_weight = request.POST.get('weight')
        
        try:
            new_weight = float(new_weight)
            if new_weight < 0:
                messages.error(request, 'Weight cannot be negative.')
                return redirect('medicalInfo')
            
            patient_profile.weight = new_weight
            patient_profile.save()
            
            messages.success(request, 'Your weight has been updated.')
            return redirect('medicalInfo')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid weight value. Please enter a valid number.')
    
    context = {
        'current_weight': patient_profile.weight,
        'page': page,
    }
    return render(request, 'account/update_personal.html', context)

@login_required
def change_language(request):
    page = "language"
    
    if request.method == 'POST':
        language = request.POST.get('language', 'en')
        next_page = request.POST.get('next','/')
        translation.activate(language) 
        if next_page == "setting":
            response = redirect('setting')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
        else:
            response = redirect(next_page)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
        
    current_language = translation.get_language()
        
    context = {
        'page': page,
        'current_language': current_language,
    }
    
    return render(request, 'account/update_setting.html', context)

def update_hospital_rating(hospital):
    new_rating = fetch_hospital_rating(hospital.name)
    if new_rating is not None:
        hospital.rating = new_rating
        hospital.updated_at = now()  # Giả sử đã thêm trường updated_at vào model Hospital
        hospital.save()

@csrf_exempt
def findHospital(request):
    if request.user.is_authenticated:
        favourite_hospitals_ids = request.user.favourite_hospitals.values_list('hospital', flat=True)
    else:
        favourite_hospitals_ids = []

    hospitals = Hospital.objects.annotate(
        is_favourite=Case(
            When(id__in=list(favourite_hospitals_ids), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).order_by('-is_favourite', 'name')

    if 'affiliated_with_insurers' in request.GET:
        hospitals = hospitals.annotate(insurance_count=Count('supported_insurance')).filter(insurance_count__gt=0)

    if 'english_speaking_staff' in request.GET:
        hospitals = hospitals.filter(supported_languages__name__icontains="English")

    user_location = ''
    if request.method == "POST":
        data = json.loads(request.body) 
        user_location = data.get('user_location', '')

        for hospital in hospitals:
            distance_info = DistanceInfo.objects.filter(hospital=hospital).first()
            if distance_info is None:
                distance_info = DistanceInfo.objects.create(hospital=hospital)
                created = True
            else:
                created = False
            
            if created or now() - distance_info.last_updated > timedelta(minutes=30):
                distance_text, duration_text = fetch_distance_and_duration(user_location, hospital.name)
                distance_info.distance_text = distance_text
                distance_info.duration_text = duration_text
                distance_info.last_updated = now()
                distance_info.save()
    
    for hospital in hospitals:
        if hospital.rating is None or now() - hospital.updated_at > timedelta(days=30): 
            update_hospital_rating(hospital)

    distance_infos = {hospital.id: {'distance_text': None, 'duration_text': None} for hospital in hospitals}
    for hospital in hospitals:
        distance_info = DistanceInfo.objects.filter(hospital=hospital).first()
        if distance_info.distance_text and ',' in distance_info.distance_text:
            distance_info.distance_text = distance_info.distance_text.replace(',', '')
        if distance_info:
            distance_infos[hospital.id] = {
                'distance_text': distance_info.distance_text,
                'duration_text': distance_info.duration_text,
            }

    context = {
        'hospitals': hospitals,
        'distance_infos': distance_infos,
        'favourite_hospitals_ids': favourite_hospitals_ids,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    return render(request, 'home/findHospital.html', context)

@login_required
def add_to_favourites(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    FavouriteHospital.objects.get_or_create(user=request.user, hospital=hospital)
    page = request.GET.get('page', 'findHospital')
    if page == "findHospital":
        return redirect('findHospital')
    if page == "hospitalInfo":
        return redirect('hospitalInfo', pk=hospital_id)
        
@login_required
def remove_from_favourites(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    FavouriteHospital.objects.filter(user=request.user, hospital=hospital).delete()
    page = request.GET.get('page', 'findHospital')
    if page == "findHospital":
        return redirect('findHospital')
    if page == "hospitalInfo":
        return redirect('hospitalInfo', pk=hospital_id)

def hospitalInfo(request, pk):
    if request.user.is_authenticated:
        favourite_hospitals_ids = request.user.favourite_hospitals.values_list('hospital', flat=True)
    else:
        favourite_hospitals_ids = []
        
    hospital = Hospital.objects.get(id=pk)

    context = {
        'hospital' : hospital,
        'favourite_hospitals_ids': favourite_hospitals_ids,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'home/hospitalInfo.html', context)

def diagnose(request, question_id=None):
    if 'history' not in request.session:
        request.session['history'] = []
    
    if request.session.get('completed', False):
        context = request.session.get('final_context', {})
        return render(request, 'home/conclusion.html', context)
    
    if question_id is None:
        question = Question.objects.get(is_first_question=True)
        request.session['current_odds'] = 1
        request.session['history'] = [question.id]
    else:
        question = get_object_or_404(Question, id=question_id)

    previous_question_id = None
    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        answer = get_object_or_404(Answer, id=answer_id)
        current_odds = request.session.get('current_odds', 1)

        if answer.likelihood_ratio:
            new_odds = current_odds * answer.likelihood_ratio
        else:
            new_odds = current_odds

        request.session['current_odds'] = new_odds
        request.session['history'].append(question.id if answer.next_question else None)
        request.session.modified = True

        if answer.is_conclusive:
            conclusions = answer.conclusions.all()
            selected_conclusion = None
            for conclusion in conclusions:
                if (new_odds >= 1 and conclusion.odds_condition == '>=1') or (new_odds < 1 and conclusion.odds_condition == '<1'):
                    selected_conclusion = conclusion.text
                    odds_conclusion = conclusion.odds_condition
                    id_conclusion = conclusion.id
                    break
            conclusion_text = selected_conclusion or "No appropriate conclusion could be determined."
        
            probability = new_odds / (1 + new_odds)
            probability_percent = "{:.2%}".format(probability)
            odds_percentage = float(probability_percent.replace('%', ''))
            context = {
                'conclusion': _(conclusion_text),
                'odds_conclusion': odds_conclusion,
                'id_conclusion': id_conclusion,
                'odds': probability_percent,
                'odds_css': odds_percentage,
            }
            request.session['completed'] = True 
            request.session['final_context'] = context
            request.session['odds_session'] = probability_percent
            request.session.modified = True
            if request.user.is_authenticated:
                SymptomCheckSession.objects.create(
                    user=request.user,
                    conclusion_text=conclusion_text,
                    odds_percentage=probability_percent,
                    id_conclusion=id_conclusion
                )
            return render(request, 'home/conclusion.html', context)
        elif answer.next_question:
            return redirect('diagnose', question_id=answer.next_question_id)
    else:
        if len(request.session['history']) > 1:
            previous_question_id = request.session['history'][-1]
    
    context = {
        'question': question,
        'previous_question_id': previous_question_id,
    }
    return render(request, 'home/question.html', context)

def conclusion_detail(request, id_conclusion):
    conclusion = Conclusion.objects.get(id=id_conclusion) if id_conclusion else None
    if request.user.is_authenticated:
        conclusion_session = SymptomCheckSession.objects.filter(id_conclusion=id_conclusion).order_by('-created_at').first() if id_conclusion else None
        odds_percentage = float(conclusion_session.odds_percentage.replace('%', ''))
    else:
        odds_percentage = float(request.session['odds_session'].replace('%', ''))

    context = {
        'conclusion': conclusion,
        'odds': odds_percentage,
    }
    return render(request, 'home/conclusion_detail.html', context)

@login_required
def history(request):
    history = SymptomCheckSession.objects.filter(user=request.user).order_by('-created_at')
    
    for his in history:
        his.conclusion_text = _(his.conclusion_text)
    
    context = {
        'histories': history
    }
    return render(request, 'home/history.html', context)

@login_required
def saved(request):
    save = FavouriteHospital.objects.filter(user=request.user)
    context = {
        'saved': save
    }
    return render(request, 'home/saved.html', context)

def filter(request):
    context = {}
    return render(request, 'home/filter.html', context)

def fetch_distance_and_duration(origin, destination):
    api_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': origin,
        'destinations': destination,
        'key': settings.GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        element = data['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance_text = element['distance']['text']
            duration_text = element['duration']['text']
            return distance_text, duration_text
    return None, None

def fetch_hospital_rating(hospital_name):
    api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': hospital_name + " hospital",
        'inputtype': 'textquery',
        'fields': 'rating',
        'key': settings.GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if data['status'] == 'OK' and data['candidates']:
        return data['candidates'][0].get('rating')
    return None



    