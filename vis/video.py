

def frames_to_video_with_ffmpeg(input_dir,output_path,img_range=(),rate=30):
    """
    note, try using ".mov" as video file extension. The extension ".avi" gives a video but it is not accepted by iMovies.
    """
    if input_dir[-1] == '/':
        input_dir = input_dir[:-1] # the trailing / messes up the name.
    _,fnames = dir_as_dic_and_list(input_dir)
    frames_folder = input_dir.split('/')[-1]
    unix('mkdir -p '+'/'.join(output_path.split('/')[:-1]))
    unix_str = ' -i '+input_dir+'/%d.png -pix_fmt yuv420p -r '+str(rate)+' -b:v 14000k '+output_path
    success = False
    try:
        print('Trying avconv.')
        unix('avconv'+unix_str)
        success = True
    except Exception as e:
        print("'avconv did not work.' ***************************************")
        print(e.message, e.args)
        print("***************************************")
    if not success:
        try:
            print('Trying ffmpeg.')
            unix('ffmpeg'+unix_str)
            success = True
        except Exception as e:
            print("'ffmeg did not work.' ***************************************")
            print(e.message, e.args)
            print("***************************************")
    if success:
        print('frames_to_video_with_ffmpeg() had success with ' + frames_folder)



∑