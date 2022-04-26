from django.urls import path,include
from .views import *
urlpatterns = [
    path('<str:name>/stream/',streamview,name='class'),
    path('<str:name>/people/',peopleview,name='people'),
    path('<str:name>/assignments/',assignments,name='assignment-list'),
    path('create-class/',createClass,name='create-class'),
    path('join',joinclass,name = 'join'),
    path('<str:name>/stream/create',createStream,name = 'create-stream'),
    path('<str:name>/stream/comment',createComment,name = 'comment-stream'),
    path('<str:name>/assignment/details',assignmentDetails,name='assignment-detail'),
    path('<str:name>/assignment/create',createAssignment,name='create-assignment'),
    path('<str:name>/leave',leaveClass,name='leave')
]
