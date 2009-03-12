from django.conf.urls.defaults import *

urlpatterns = patterns('albastryde.ajax_comments.views',
    url(r'^comment/post/$',
        view='ajax_comment_post',
        name='ajax_comment_post'),
)

