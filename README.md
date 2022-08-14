# visitor_servc_robot
Visitor Service Robot Hardware controller and OpenCV + Keras based mask detection
############################ MOTION ############################

[CMD]                           [RESP]

hi_start_motion                 hi_start_complete
hi_end_motion                   hi_end_complete

sanitizer_start_motion          sanitizer_start_complete
sanitizer_end_motion            sanitizer_end_complete

mask_get_motion                 mask_get_complete
mask_give_motion                mask_give_complete

namaste_start_motion            namaste_start_complete
namaste_end_motion              namaste_end_complete

goto_normal_motion              goto_normal_complete


################### Streaming ###########################

Topic  : 'streaming'
payload : '0' or '1'

Topic : 'mask_result_tmpr'
payload : 'mask result, temperature'
