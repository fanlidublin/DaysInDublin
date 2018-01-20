# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from courses.models import CourseOrg, Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_cities = CityDict.objects.all()

        # 搜索查找功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(name__icontains=search_keywords)

        # 筛选类别
        category = request.GET.get('cat', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 页面机构数统计
        org_nums = all_orgs.count()

        # 分页
        try:
            page = request.GET.get('page', 1)

        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


class OrgHomeView(View):
    def get(self, request, org_id):
        current = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # judge fav
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:4]
        all_techers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_techers': all_techers,
            'course_org': course_org,
            'current': current,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # judge fav
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'course_org': course_org,
            'all_courses': all_courses,
            'current': current,
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # judge fav
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current': current,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # judge fav
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_techers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_techers': all_techers,
            'current': current,
            'has_fav': has_fav
        })


# 收藏功能公用接口
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            return HttpResponse('{ "status" : "fail", "msg": "用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            exist_record.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{ "status" : "success", "msg": "收藏"}', content_type='application/json')
        else:
            favorite = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                favorite.user = request.user
                favorite.fav_id = int(fav_id)
                favorite.fav_type = int(fav_type)
                favorite.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{ "status" : "success", "msg": "已经收藏"}', content_type='application/json')
            else:
                return HttpResponse('{ "status" : "fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teachers_nums = Teacher.objects.all().count()

        # 搜索查找功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(name__icontains=search_keywords)
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)

        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 2, request=request)

        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'teachers_nums': teachers_nums,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav = True

        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'all_courses': all_courses,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav
        })
