from django.urls import path, include
from rest_framework.routers import DefaultRouter
from googledriveapp.api.views import (GoogleAuthCode, GoogleRefreshToken,
                                      GoogleDriveFolders, GoogleDriveFileDownload,
                                      GoogleRegenerateRefreshToken
                                      )

router = DefaultRouter()

router.register('auth-code', GoogleAuthCode, basename='auth_code')
router.register('token', GoogleRefreshToken, basename='token')
router.register('refresh-token', GoogleRegenerateRefreshToken, basename='re-generate_token')
router.register('drive/folders', GoogleDriveFolders, basename='drive_folders')
router.register('drive/files', GoogleDriveFileDownload, basename='drive_file_download')

urlpatterns = [
    path('', include(router.urls)),
]
