# -*- coding: utf-8 -*-
from org.tools import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import Lawyer, Client, Remark, Activity
from products.models import Order,Comment
from questions.models import Question,EnumQuestionState
from org.settings import RSA_LOGIN_KEY
from org.rsa_authentication import decrypt

class RegisterForm(forms.Form):
	username = forms.CharField(label="账户",max_length=254)
	last_name = forms.CharField(label="姓",max_length=20)
	first_name = forms.CharField(label="名",max_length=20)
	email = forms.EmailField(label="邮箱")
	password = forms.CharField(label="密码", widget=forms.PasswordInput)
	password_confirm = forms.CharField(label="密码确认", widget=forms.PasswordInput)

def login_view(request): # [UnitTest]
	if request.method=='POST':
		username,password = request.POST['username'],request.POST['password']
		next_url = request.POST['next'] if 'next' in request.POST else reverse('index:index')
		user = authenticate(username=username, password=password)
		rec=recorded(request,'login')
		if user is not None:
			login(request, user)
			rec.success(u'{0}登入成功'.format(username))  # [UnitTest]
			return response_jquery({'r':'success','redirect':next_url})
		else: 
			rec.error(u'{0}登入失败'.format(username))  # [UnitTest]
			return response_jquery({'r':'error'})
	else:
		if request.user.is_authenticated():
			return redirect("index:index")
		else:  
			return response(request, 'accounts/login.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def siege_view(request):
	# $.post('/accounts/login4siege/',{username:'lawyer0',password:'1234'});
	# siege -A "org-under-siege" "http://localhost:8000/accounts/login4siege/ POST username=lawyer0&password=1234"
	if request.method=='POST' and request.META['HTTP_USER_AGENT']=="org-under-siege":
		username,password = request.POST['username'],request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None: login(request, user)
		return HttpResponse('HELLO')
	else: raise Http404

def logout_view(request):
	logout(request)
	return redirect('index:index')

def register_view(request, role): # [UnitTest]
	if request.method=='POST':
		rec=recorded(request,'accounts:register')
		pubkey, privkey = RSA_LOGIN_KEY
		pw = decrypt(request.POST['password'].decode('hex'), privkey)
		try:
			username,profile=request.POST['username'],dict(
				password=pw,
				email=request.POST['email'],
				last_name = request.POST['last_name'],
				first_name = request.POST['first_name'],
			)
			if role=='client': 
				Client.objects.register(username,**profile)
			elif role=='lawyer': 
				Lawyer.objects.register(username,**profile)
		except: 
			messages.error(request, u'注册失败') # [UnitTest]
			rec.error(u'{0}注册失败'.format(username))
			return response_jquery({'r':'error'})
		else: 
			messages.success(request, u'注册成功')
			rec.success(u'{0}注册成功'.format(username)) # [UnitTest]
			return response_jquery({'r':'success'})
		return redirect('accounts:login')
	else: return response(request, 'accounts/register.html', register_form=RegisterForm())

def lawyerlist_view(request):
	return response(request, 'accounts/lawyerlist.html',
		lawyers=Lawyer.objects.all())

@login_required
def usercenter_view(request):
	u = get_role(request.user)
	if type(u) is Client or type(u) is Lawyer:
		return response(request, 'accounts/usercenter.html',
			activities = request.user.activity_set.all()
		)
	else: raise Http404

@login_required
def new_activities_counts_view(request):
	return response_jquery(list(Activity.objects.count_new_activities(request.user.id)))

@login_required
def questions_view(request):
	u = get_role(request.user)
	is_client = (type(u) is Client)
	qs = Question.objects.filter(state=EnumQuestionState.OPEN)
	if type(u) is Client or type(u) is Lawyer:
		return response(request, 'accounts/question_list.html',
			questions=paginated(lambda: request.GET.get('page'), 10, 
					u.question_set.order_by('-publish_date')),
			is_client=is_client,
			qs_all = qs)
	else: raise Http404

@login_required
def orders_view(request):
	u = get_role(request.user)
	print u
	if type(u) is Client or type(u) is Lawyer:
		return response(request, 'accounts/order_list.html',
			orders=paginated(lambda: request.GET.get('page'), 10, 
				u.order_set.order_by('-publish_date')),test=True)
	else: raise Http404

class ProfileEditForm(forms.ModelForm):
	avatar = forms.ImageField(required=False)

	class Meta:
		model = User
		fields = ['last_name', 'first_name', 'email', 'avatar']

@login_required
def profile_self_view(request):
	if request.method=='POST':
		form=ProfileEditForm(request.POST, request.FILES, instance=request.user)
		form.save()
		u = get_role(request.user)
		if (type(u) is Client or type(u) is Lawyer) and form.cleaned_data['avatar']:
			u.avatar = form.cleaned_data['avatar']
			u.save()
		messages.success(request, u'个人资料编辑成功')
		return redirect('accounts:profile_self')
	else: return response(request, 'accounts/profile.html', 
		role=get_role(request.user), 
		is_master=True,
		profile_edit=ProfileEditForm(instance=request.user))

def profile_view(request, pk_user):
	user = get_object_or_404(User, pk=pk_user)
	u = get_role(user)
	if request.user.id==user.id: 
		bMaster=True
	else:
		bMaster=False
	from blogs.models import BlogComment
	remark_count = BlogComment.objects.filter(user_id=user.id).count()
	remark_count += Comment.objects.filter(user_id=user.id).count()

	recent_act = Activity.objects.tagged_one('C').filter(user_id=user.id)[:10]
	#print (recent_act[0].publish_date.strftime)
	if type(u) is Client or type(u) is Lawyer:
		d = datetime.now() - get_role(u).register_date
		return response(request, 'accounts/other_profile.html',
		role=u,
		is_master=bMaster,
		act_days=d.days,
		remark_counts=remark_count,
		activities=recent_act)
	else: raise Http404

from decimal import Decimal
@login_required
def balance_view(request):
	u = get_role(request.user)
	if request.method=='POST':
		try:
			u.balance+=Decimal(request.POST['amount'])
			u.save()
			messages.success(request, u'充值成功')
		except: messages.error(request, u'充值失败')
		return redirect('accounts:balance')
	else: return response(request, 'accounts/balance.html', role=u)

@login_required
def pay_view(request, pk_order):
	order = get_object_or_404(Order, pk=pk_order)
	if request.method=='POST':
		request.POST['bankid']
		messages.success(request, u'支付成功')
		return redirect('accounts:order_list')
	else: return response(request, 'accounts/pay.html', order=order)

class RemarkForm(forms.ModelForm):
	class Meta:
		model = Remark
		fields = ['grade']

@login_required
def remark_view(request, pk_lawyer):
	lawyer = get_object_or_404(Lawyer, pk=pk_lawyer)
	remark, created = Remark.objects.get_or_create(client=request.user.client,lawyer=lawyer)
	if request.method=='POST':
		try:
			remark.grade=int(request.POST['grade'])
			remark.save()
			messages.success(request, u'评价成功')
		except: messages.error(request, u'评价失败')
		return redirect('accounts:remark', pk_lawyer=pk_lawyer)
	else: 
		return response(request, 'accounts/remark.html', 
			remark=remark,
			remark_form=RemarkForm(instance=remark), 
		)
