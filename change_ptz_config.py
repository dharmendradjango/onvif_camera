from onvif import ONVIFCamera

# Initialize the ONVIF client
camera = ONVIFCamera('192.168.1.100', 80, 'username', 'password', '/path/to/wsdl/')

# Create PTZ service
ptz_service = camera.create_ptz_service()

# Get all PTZ configurations
ptz_configurations_list = ptz_service.GetConfigurations()

# Ensure there's at least one configuration
if not ptz_configurations_list:
    raise Exception("No PTZ configurations found.")

# Copy the first PTZ configuration
ptz_configuration = ptz_configurations_list[0]

# Get PTZ configuration options
ptz_configuration_options = ptz_service.GetConfigurationOptions(ptz_configuration.token)

# Update the DefaultAbsolutePanTiltPositionSpace if possible
if len(ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace) >= 2:
    ptz_configuration.DefaultAbsolutePantTiltPositionSpace = (
        ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[1].URI
    )

# Update the DefaultAbsoluteZoomPositionSpace if possible
if len(ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace) >= 2:
    ptz_configuration.DefaultAbsoluteZoomPositionSpace = (
        ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[1].URI
    )

# Update the DefaultPTZSpeed for Pan/Tilt
if len(ptz_configuration_options.Spaces.PanTiltSpeedSpace) >= 2:
    ptz_configuration.DefaultPTZSpeed = {
        "PanTilt": {
            "x": ptz_configuration_options.Spaces.PanTiltSpeedSpace[1].XRange.Max,
            "y": ptz_configuration_options.Spaces.PanTiltSpeedSpace[1].YRange.Max,
            "space": ptz_configuration_options.Spaces.PanTiltSpeedSpace[1].URI,
        }
    }

# Update the DefaultPTZSpeed for Zoom
if len(ptz_configuration_options.Spaces.ZoomSpeedSpace) >= 2:
    ptz_configuration.DefaultPTZSpeed["Zoom"] = {
        "x": ptz_configuration_options.Spaces.ZoomSpeedSpace[1].XRange.Max,
        "space": ptz_configuration_options.Spaces.ZoomSpeedSpace[1].URI,
    }

# Apply the updated PTZ configuration
force_persistence = False
ptz_service.SetConfiguration(ptz_configuration, force_persistence)

print("PTZ configuration updated successfully.")
