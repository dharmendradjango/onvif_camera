# from onvif import ONVIFCamera

# def media_profile_configuration(ip, port, user, password):
#     """
#     Configures the media profile of an ONVIF camera.
#     Sets the video encoder to H.264 with appropriate resolution, frame rate, and bitrate.
#     """

#     try:
#         print(f"[INFO] Connecting to ONVIF Camera at {ip}:{port}...")
#         mycam = ONVIFCamera(ip, port, user, password)
#         media_service = mycam.create_media_service()

#         print("[INFO] Fetching available profiles...")
#         profiles = media_service.GetProfiles()
#         if not profiles:
#             print("[ERROR] No ONVIF profiles found on the camera!")
#             return

        
#         token = profiles[3].token
#         print(f"[INFO] Using Profile Token: {token}")

        
#         configurations_list = media_service.GetVideoEncoderConfigurations()
#         if not configurations_list:
#             print("[ERROR] No video encoder configurations found!")
#             return

        
#         video_encoder_configuration = configurations_list[0]

        
#         options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken': token})

        
#         if not hasattr(options, 'H264') or not options.H264.ResolutionsAvailable:
#             print("[WARNING] No H264 resolution options available! Using default values.")
#             width, height = 2560, 1790  
#         else:
#             width, height = options.H264.ResolutionsAvailable[0].width, options.H264.ResolutionsAvailable[0].height
#             print(f"[INFO] Available Resolutions: {[(r.width, r.height) for r in options.H264.ResolutionsAvailable]}")

        
#         video_encoder_configuration.Encoding = 'H264'
#         video_encoder_configuration.Resolution.width = width
#         video_encoder_configuration.Resolution.height = height
#         video_encoder_configuration.Quality = getattr(options, 'QualityRange', None).Min if hasattr(options, 'QualityRange') else 5  # Default quality

        
#         if hasattr(options.H264, 'FrameRateRange'):
#             video_encoder_configuration.RateControl.FrameRateLimit = options.H264.FrameRateRange.Min
#         else:
#             video_encoder_configuration.RateControl.FrameRateLimit = 15  
       
#         if hasattr(options.H264, 'EncodingIntervalRange'):
#             video_encoder_configuration.RateControl.EncodingInterval = options.H264.EncodingIntervalRange.Min
#         else:
#             video_encoder_configuration.RateControl.EncodingInterval = 1  
        
#         if hasattr(options.Extension, 'H264') and hasattr(options.Extension.H264[0], 'BitrateRange'):
#             video_encoder_configuration.RateControl.BitrateLimit = options.Extension.H264[0].BitrateRange[0].Min[0]
#         else:
#             video_encoder_configuration.RateControl.BitrateLimit = 500  

        
#         request = media_service.create_type('SetVideoEncoderConfiguration')
#         request.Configuration = video_encoder_configuration
#         request.ForcePersistence = True  

        
#         print("[INFO] Setting new video encoder configuration...")
#         media_service.SetVideoEncoderConfiguration(request)
#         print("[SUCCESS] Video encoder configuration updated successfully!")

        
#         updated_config = media_service.GetVideoEncoderConfiguration({'ConfigurationToken': video_encoder_configuration.token})
#         print("[INFO] Updated Configuration:")
#         print(f"  Encoding: {updated_config.Encoding}")
#         print(f"  Resolution: {updated_config.Resolution.width}x{updated_config.Resolution.height}")
#         print(f"  Frame Rate: {updated_config.RateControl.FrameRateLimit}")
#         print(f"  Bitrate: {updated_config.RateControl.BitrateLimit}")

#     except Exception as e:
#         print(f"[ERROR] Failed to configure the media profile: {str(e)}")


# if __name__ == '__main__':
    
#     IP = "14.195.152.243"
#     PORT = 80
#     USER = "admin"
#     PASSWORD = "admin@123"

#     media_profile_configuration(IP, PORT, USER, PASSWORD)









from onvif import ONVIFCamera


camera_ip = '14.195.152.243'
port = 80
username = 'admin'
password = 'admin@123'


camera = ONVIFCamera(camera_ip, port, username, password)

media_service = camera.create_media_service()

profiles = media_service.GetProfiles()
if not profiles:
    raise Exception("No profiles found on the camera.")


profile = profiles[3]
print(profile)

# Get current video source configuration
video_source_config = media_service.GetVideoSourceConfiguration(profile.VideoSourceConfiguration.token)
if not video_source_config:
    raise Exception("Failed to get video source configuration.")


video_source_config.Bounds.width = 2021  
video_source_config.Bounds.height = 1080  


request = media_service.create_type('SetVideoSourceConfiguration')
request.Configuration = video_source_config  
request.ForcePersistence = True  

# Apply new configuration
media_service.SetVideoSourceConfiguration(request)

print(f"✅ Video configuration updated successfully to {video_source_config.Bounds.width}x{video_source_config.Bounds.height}")











# from onvif import ONVIFCamera


# camera_ip = '14.195.152.243'
# port = 80
# username = 'admin'
# password = 'admin@123'


# camera = ONVIFCamera(camera_ip, port, username, password)

# media_service = camera.create_media_service()

# profiles = media_service.GetProfiles()
# if not profiles:
#     raise Exception("No profiles found on the camera.")


# profile = profiles[3]

# # Get current video source configuration
# video_source_config = media_service.GetVideoSourceConfiguration(profile.VideoSourceConfiguration.token)
# if not video_source_config:
#     raise Exception("Failed to get video source configuration.")


# video_source_config.Bounds.width = 2021  
# video_source_config.Bounds.height = 1080  


# request = media_service.create_type('SetVideoSourceConfiguration')
# request.Configuration = video_source_config  
# request.ForcePersistence = True  

# # Apply new configuration
# media_service.SetVideoSourceConfiguration(request)

# print(f"✅ Video configuration updated successfully to {video_source_config.Bounds.width}x{video_source_config.Bounds.height}")
