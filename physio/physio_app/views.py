import simplejson
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core import serializers

from .models import contact, feedback, physio_master, appointment, patient_master, state, city, \
    area, complaint, degree, specialization, \
    security_question, tips, treatment, posts


# Create your views here.
def home(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            physio_list = physio_master.objects.all().order_by('id')[:3]
            return render(request, "Physio/home.html", {'physio_list': physio_list})
        else:
            messages.error(request, 'Only Physiotherapist can access that Page')
            return redirect('home')
    else:
        messages.error(request, 'You must login as physiotherapist')
        return redirect('login')


def base(request):
    return render(request, "base_patient.html")


def post_tips(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            treatment_list = treatment.objects.all()
            tips_list = tips.objects.filter(physio_id=request.session['id'])
            return render(request, 'Physio/tipsform.html', {'treatment_list': treatment_list,
                                                            'tips_list': tips_list})
        else:
            messages.error(request, 'Only Physiotherapist can access that Page')
            return redirect('home')
    else:
        messages.error(request, 'You must login as physiotherapist')
        return redirect('login')


def tips_success(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            if request.method == 'POST':
                # return render(request, 'success.html', {'id':id,'title':request.POST['title'],'desc':request.POST['description'],'treatment_id':request.POST['treatment_id']})
                s = tips(physio_id_id=request.session['id'], tips_title=request.POST['title'],
                         description=request.POST['description'],
                         treatment_id_id=request.POST['treatment_id'])
                s.save()
                return redirect('post_tips')
            else:
                messages.error(request, 'No Data Recieved')
                return redirect('post_tips')
        else:
            messages.error(request, 'Only physiotherapist can access that page')
            return redirect('login')
    else:
        messages.error(request, 'You must login as physiotherapist')
        return redirect('login')


def photo_tips(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            treatment_list = treatment.objects.all()
            tips_list = tips.objects.all()
            return render(request, 'Physio/photoform.html', {'treatment_list': treatment_list, 'tips_list': tips_list})
        else:
            messages.error(request, 'Only Physiotherapist can access that Page')
            return redirect('home')
    else:
        messages.error(request, 'You must login as physiotherapist')
        return redirect('login')


def p_manage_profile(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            state_list = state.objects.all()
            city_list = city.objects.all()
            area_list = area.objects.all()
            sec_que_list = security_question.objects.all()
            user = physio_master.objects.get(id=request.session['id'])
            return render(request, 'Physio/manageProfile.html', {'user': user,
                                                                 'state_list': state_list,
                                                                 'city_list': city_list,
                                                                 'area_list': area_list,
                                                                 'sec_que_list': sec_que_list})
        else:
            messages.error(request, 'only physiotherapist can access that page')
            return redirect('home')
    else:
        messages.error(request, 'You must login as physiotherapist')
        return redirect('login')


def manage_success(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            if request.method == 'POST':
                if request.FILES['image'] != '':
                    return render(request, 'success.html', {'image': request.FILES['image']})
    #                 file = request.FILES['file']
    #                 fs = FileSystemStorage()
    #                 filename = fs.save('physio/profile/' + file.name, file)
    #                 f_url = fs.url(filename)
    #                 s = physio_master.objects.filter(id=request.session['id']).update(image=f_url)
    #             s = physio_master.objects.filter(id=request.session['id']).update(first_name=request.POST['p_fname'],
    #                                                                               last_name=request.POST['p_lname'],
    #                                                                               password=request.POST['password'],
    #                                                                               dob=request.POST['dob'],
    #                                                                               area_id_id=request.POST['area'],
    #                                                                               city_id_id=request.POST['city'],
    #                                                                               state_id_id=request.POST['state'],
    #                                                                               address=request.POST['address'],
    #                                                                               email=request.POST['email'],
    #                                                                               ph_no=request.POST['ph_no'],
    #                                                                               security_que_id_id=request.POST[
    #                                                                                   'sec_que'],
    #                                                                               ans=request.POST['ans'])
    return redirect('physio_home')


def photo_success(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            if request.method == 'POST' and request.FILES['media_tips']:
                file = request.FILES['media_tips']
                fs = FileSystemStorage()
                filename = fs.save("physio/media_tips/" + file.name, file)
                f_url = fs.url(filename)
                s = posts(physio_id_id=request.session['id'],
                          post_title=request.POST['name'],
                          video_photo=f_url,
                          treatment_id_id=request.POST['treatment_id'],
                          description=request.POST['message'],
                          type=request.POST['type'])
                s.save()
                return redirect('photo_tips')
            else:
                messages.error('No Data Recieved')
                return redirect('post_tips')
        else:
            messages.error('Only physiotherapist can access that page')
            return redirect('login')
    else:
        messages.error('You must login as physiotherapist')
        return redirect('login')


def p_about(request):
    return render(request, 'Physio/about.html')


def p_recruit(request):
    return render(request, 'Physio/recriutment_post.html')


def p_appointment(request):
    appointment_list = appointment.objects.filter(physio_id=request.session['id'])
    return render(request, 'Physio/appointment.html', {'appointment_list': appointment_list})


def home_page(request):
    physio_list = physio_master.objects.all().order_by('id')[:3]
    return render(request, "Patient/home.html", {'physio_list': physio_list})


def about(request):
    return render(request, 'Patient/about.html')


def appointments(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            treatment_list = treatment.objects.all()
            physio = physio_master.objects.get(id=id)
            user = patient_master.objects.get(id=request.session['id'])
            messages.success(request,'Appointment successfully requested')
            return render(request, 'Patient/appointment.html', {'treatment_list': treatment_list,
                                                                'physio': physio,
                                                                'user': user})
        else:
            messages.error(request, 'only patients can take request for appointment')
            return redirect('physio_home')
    else:
        messages.error(request, 'you must login as patient to request for an appointment')
        return redirect('login')


def appointment_success(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            if request.method == 'POST':
                physio = physio_master.objects.get(id=id)
                # pa=request.session['id']
                # ph=treatment_id
                # ti= request.POST['Time']
                # da= request.POST['Date']
                # pd= request.POST['form_message']
                # return render(request,'success.html',{'pa':pa,'ph':ph,'ti':ti,'da':da,'pd':pd})
                s = appointment(patient_id_id=request.session['id'],
                                physio_id_id=id, time=request.POST['Time'],
                                date_of_appointment=request.POST['Date'],
                                treatment_id_id=request.POST['treatment_id'],
                                patient_description=request.POST['form_message'],
                                )
                s.save()
                print(s)
                # return render(request, 'Patient/appointment.html', {'iid': id})
                return redirect('appointments',id)
            else:
                messages.error(request,'No Data Recieved')
                return redirect('appointments')
        else:
            messages.error(request, 'Only patient can access that page')
            return redirect('login')
    else:
        messages.error(request, 'You must login as patient')
        return redirect('login')


def booked(request):
    return render(request, 'Patient/appointment.html')


def complaints(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            physio = physio_master.objects.get(id=id)
            user = patient_master.objects.get(id=request.session['id'])
            return render(request, 'Patient/complaint.html', {'user': user, 'physio': physio})
        else:
            messages.error(request, 'only patients can complaint')
            return redirect('physio_home')
    else:
        messages.error(request, 'you must login as patient to complaint')
        return redirect('login')


def complaint_success(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            if request.method == 'POST':
                physio = physio_master.objects.get(id=id)
                s = complaint(physio_id_id=physio,
                              patient_id_id=request.session['id'],
                              description=request.POST['description'])
                s.save()
                return redirect('complaints')
            else:
                messages.error(request, 'No Data Recieved')
                return redirect('post_tips')
        else:
            messages.error(request, 'Only patient can access that page')
            return redirect('login')
    else:
        messages.error(request, 'You must login as patient')
        return redirect('login')


def contact_view(request):
    return render(request, 'Patient/contact.html')


def contact_success(request):
    context = {
        "title": "Contacts",
        "content": "Data Inserted Successfully",
        "post": request.POST,
    }
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        s = contact(user_name=name, email=email, ph_no=phone, address=message)
        s.save()
    return render(request, 'Patient/home.html', messages.success(request, 'We will Contact you later'))


def feedbacks(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            user = patient_master.objects.get(id=request.session['id'])
            return render(request, 'Patient/feedback.html', {'user': user})
        else:
            messages.error(request, 'only patients can give feedback')
            return redirect('physio_home')
    else:
        messages.error(request, 'you must login as patient to give feedback')
        return redirect('login')


def feedback_success(request, id):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            if request.method == 'POST':
                s = feedback(patient_id_id=request.session['id'],
                             description=request.POST['description'])
                s.save()
                return redirect('feedbacks')
            else:
                messages.error(request, 'No Data Recieved')
                return redirect('post_tips')
        else:
            messages.error(request, 'Only patient can access that page')
            return redirect('login')
    else:
        messages.error(request, 'You must login as patient')
        return redirect('login')


def login(request):
    s = security_question.objects.all()
    return render(request, 'Patient/index.html',{'sec':s})


def login_patient(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        c = patient_master.objects.filter(email=email, password=password).count()
        if c == 1:
            data = patient_master.objects.get(email=email, password=password)
            request.session['id'] = data.id
            request.session['email'] = data.email
            request.session['is_login'] = 1
            request.session['user_type'] = 'patient'
            return redirect('home')
        else:
            messages.error(request, 'Password Or Email are incorrect...')
            return render(request, 'Patient/index.html')


def logout(request):
    del request.session['id']
    del request.session['email']
    del request.session['is_login']
    del request.session['user_type']
    return redirect("login")


def login_physio(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        c = physio_master.objects.filter(email=email, password=password).count()
        if c == 1:
            data = physio_master.objects.get(email=email, password=password)
            request.session['id'] = data.id
            request.session['email'] = data.email
            request.session['is_login'] = 1
            request.session['user_type'] = 'physio'
            return redirect('physio_home')
        else:
            messages.error(request, 'Password Or Email are incorrect...')
            return render(request, 'Patient/index.html')


def tips_view(request):
    tips_list = tips.objects.all()
    return render(request, 'Patient/tips.html', {'tips_list': tips_list})


def treatments(request):
    treatment_list = treatment.objects.all()
    return render(request, 'Patient/service.html', {'treatment_list': treatment_list})


def photo_video(request):
    media_list = posts.objects.all()
    return render(request, 'Patient/photo_video.html', {'media_list': media_list})


def physio_register(request):
    state_list = state.objects.all()
    # city_list = city.objects.all()
    # area_list = area.objects.all()
    degree_list = degree.objects.all()
    # specialization_list = specialization.objects.all()
    sec_que_list = security_question.objects.all()
    return render(request, "Physio/physio_register.html", {'state_list': state_list,
                                                           'degree_list': degree_list,
                                                           'sec_que_list': sec_que_list})


def physio_register_success(request):
    if request.method == "POST" and request.FILES['image'] and request.FILES['document']:
        p_lname = request.POST['p_lname']
        password = request.POST['password']
        dob = request.POST['dob']
        email = request.POST['email']
        mobile = request.POST['mobile']
        experience = request.POST['experience']
        address = request.POST['Address']
        # image = request.POST['image']
        # document = request.POST['document']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        degree = request.POST['degree']
        specialization = request.POST['specialization']
        seq_que = request.POST['seq_que']
        answer = request.POST['answer']
        file = request.FILES['image']
        doc = request.FILES['document']
        fs = FileSystemStorage()
        profile_name = fs.save('physio/profile/' + file.name, file)
        fss = FileSystemStorage()
        profile_url = fs.url(profile_name)
        document_name = fss.save('physio/proof_images/' + doc.name, doc)
        document_url = fss.url(document_name)
        s = physio_master(first_name=request.POST['p_fname'], last_name=p_lname,
                          password=password, dob=dob,
                          area_id_id=area, city_id_id=city,
                          state_id_id=state, address=address, email=email,
                          ph_no=mobile, gender=request.POST['Gender'],
                          image=profile_url, degree_id_id=degree,
                          specialization_id_id=specialization,
                          experience=experience, proof_image=document_url,
                          security_que_id_id=seq_que, ans=answer)
        s.save()
        messages.success(request, "Registered successfully..")
    return redirect('home')


def patient_register(request):
    state_list = state.objects.all()
    city_list = city.objects.all()
    area_list = area.objects.all()
    sec_que_list = security_question.objects.all()
    return render(request, "Patient/patient_register.html", {'state_list': state_list, 'city_list': city_list,
                                                             'area_list': area_list,
                                                             'sec_que_list': sec_que_list})


def patient_register_success(request):
    if request.method == "POST" and request.FILES['image']:
        mobile = request.POST['mobile']
        # image = request.POST['image']
        address = request.POST['Address']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        seq_que = request.POST['sec_que']
        answer = request.POST['answer']
        file = request.FILES['image']
        if request.POST['password'] != request.POST['cpassword']:
            return render(request, 'patient/patient_register.html',
                          messages.error("Password and confirm password are not same"))
        fs = FileSystemStorage()
        filename = fs.save("patient/profile/" + file.name, file)
        f_url = fs.url(filename)
        s = patient_master(first_name=request.POST['p_fname'],
                           last_name=request.POST['p_lname'],
                           password=request.POST['password'],
                           address=address, area_id_id=area,
                           city_id_id=city, state_id_id=state,
                           dob=request.POST['dob'], age=request.POST['age'],
                           email=request.POST['email'], ph_no=mobile,
                           gender=request.POST['Gender'], image=f_url,
                           security_que_id_id=seq_que, ans=answer)
        s.save()
        messages.success(request, 'You are registered as patient successfully')
        return redirect('home')


def physio_list(request):
    physiolist = physio_master.objects.all()
    return render(request, 'Patient/physio_list.html', {'physiolist': physiolist})


def physio_detail(request, id):
    try:
        physio = physio_master.objects.get(id=id)
    except physio_master.DoesNotExist:
        raise Http404('Physio not available')
    return render(request, 'Patient/physio_detail.html', {'physio': physio})


# def demo_file_upload(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         fs = FileSystemStorage()
#         filename = fs.save("physio/images/"+file.name, file)
#         url = fs.url(filename)
#
#         return render(request,'success.html',{'url':url})
#     return render(request,'demo_file_upload.html')


def manage_profile(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'patient':
            state_list = state.objects.all()
            city_list = city.objects.all()
            area_list = area.objects.all()
            sec_que_list = security_question.objects.all()
            user = patient_master.objects.get(id=request.session['id'])
            return render(request, 'Patient/manageProfile.html',
                          context={'user': user,
                                   'state_list': state_list,
                                   'city_list': city_list,
                                   'area_list': area_list,
                                   'sec_que_list': sec_que_list})
        else:
            messages.error(request, 'only patient can access that page')
            return redirect('home')
    else:
        messages.error(request, 'You must login as patient')
        return redirect('login')


def edit_success(request):
    if request.session.has_key('user_type'):
        if request.session['user_type'] == 'physio':
            if request.method == 'POST':
                if request.FILES['image'] is not None:
                    file = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save('patient/profile/' + file.name, file)
                    f_url = fs.url(filename)
                    s = patient_master.objects.filter(id=request.session['id']).update(image=f_url)
                s = patient_master.objects.filter(id=request.session['id']).update(first_name=request.POST['p_fname'],
                                                                                   last_name=request.POST['p_lname'],
                                                                                   password=request.POST['password'],
                                                                                   dob=request.POST['dob'],
                                                                                   area_id_id=request.POST['area'],
                                                                                   city_id_id=request.POST['city'],
                                                                                   state_id_id=request.POST['state'],
                                                                                   address=request.POST['address'],
                                                                                   email=request.POST['email'],
                                                                                   ph_no=request.POST['ph_no'],
                                                                                   security_que_id_id=request.POST[
                                                                                       'sec_que'],
                                                                                   ans=request.POST['ans'])
                messages.success(request, 'Your profile edited successfully')
    return redirect('home')


def sunday_tips(request):
    sundaytips = tips.objects.filter(pub_date__week_day=1)
    mondaytips = tips.objects.filter(pub_date__week_day=2)
    tuesdaytips = tips.objects.filter(pub_date__week_day=3)
    wedtips = tips.objects.filter(pub_date__week_day=4)
    thurtips = tips.objects.filter(pub_date__week_day=5)
    fritips = tips.objects.filter(pub_date__week_day=6)
    sattips = tips.objects.filter(pub_date__week_day=7)
    print(sundaytips)
    print(mondaytips)
    print(tuesdaytips)
    print(wedtips)
    print(thurtips)
    print(fritips)
    print(sattips)
    return render(request,'Patient/tips.html',{'sundaytips':sundaytips,'mondaytips':mondaytips,
                                               'tuesdaytips':tuesdaytips,'wedtips':wedtips,
                                               'thurtips':thurtips,'fritips':fritips,
                                               'sattips':sattips})


def state_ajax(request):
        if request.method == 'POST':
            sid = request.POST['sid']
            citylist = city.objects.filter(state_id_id=sid).values_list('id','city_name')

            cid = list(citylist)
            print(cid)
            for value in cid:
                print(value)
                print(value[0], value[1])
                ciid = value[0]
                cname = value[1]
                print(ciid)
                print(cname)
                # res =res +  "<option value="+str(ciid)+">"+cname+"</option>"
                # return JsonResponse(res,safe=False)
                return JsonResponse("<option value="+str(ciid)+">"+cname+"</option>", safe=False)


def city_ajax(request):
        if request.method == 'POST':
            cd = request.POST['cd']
            arealist = area.objects.filter(state_id_id=cd).values_list('id','city_name')

            cid = list(arealist)
            print(cid)
            for value in cid:
                print(value)
                print(value[0], value[1])
                ciid = value[0]
                cname = value[1]
                print(ciid)
                print(cname)
                # res =res +  "<option value="+str(ciid)+">"+cname+"</option>"
                # return JsonResponse(res,safe=False)
                return JsonResponse("<option value="+str(ciid)+">"+cname+"</option>", safe=False)


def checkMail(request):
    if request.method == 'GET' and request.is_ajax():
        formemail = request.GET.get('email')
        if patient_master.objects.filter(email=formemail).exists():
            return True
        else :
            message = messages.error(request,"Email already registered.")
            response = JsonResponse({'status':'false','message':message}, status=500)
            return response


def approve_ajax(request):
    if request.method == 'POST':
        s = appointment.objects.filter(patient_id=request.POST.get('patid')).update(is_active=request.POST.get('app'))
        message = messages.success(request,"Appointment Approved");
        return JsonResponse({'message':message,'s':s})
