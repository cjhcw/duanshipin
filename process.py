import os
import time

def getJoinedPath(dir_path):
    cmds = []
    params = ''
    for file in os.listdir(dir_path):
        if params != '':
            params += '|'
        new_file = file.replace('mp4', 'ts')
        params += new_file
        single_cmd = 'ffmpeg -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s' % (file, new_file)
        cmds.append(single_cmd)
    merge_cmd = 'ffmpeg -i "concat:%s" -c copy -bsf:a aac_adtstoasc -movflags +faststart output.mp4' % params
    cmds.append(merge_cmd)
    return cmds

def write_videos(dir_path):
    os.chdir(dir_path)
    f = open('filelist.txt', 'w', encoding='utf-8')
    for file in os.listdir(dir_path):
        index = file.find('txt')
        if index != -1:
            continue
        file_name = file.rsplit('.', 1)[0]
        new_file = '{}.MTS'.format(file_name)
        if not os.path.exists(os.path.join(dir_path, new_file)):
            cmd = 'ffmpeg -i {} -q 0 {}'.format(file, new_file)
            os.system(cmd)
        str = 'file \'{}\''.format(new_file)
        f.writelines(str)
        f.write('\n')
    f.close()

def getAllVideosInfo(dir_path):
    os.chdir(dir_path)
    for file in os.listdir(dir_path):
        cmd = 'ffmpeg -i %s' % file
        os.system(cmd)
        time.sleep(1)

def merge_videos(dir_path=''):
    dir_path = os.getcwd()
    write_videos(dir_path)
    os.chdir(dir_path)
    des_name = 'output.MTS'
    if not os.path.exists(os.path.join(dir_path, des_name)):
        cmd = 'ffmpeg -f concat -safe 0 -i filelist.txt -c copy {}'.format(des_name)
        os.system(cmd)
        time.sleep(1)
    for file in os.listdir(dir_path):
        print(file)
        if file == des_name:
            os.rename(os.path.join(dir_path, des_name), os.path.join(dir_path, 'output.mp4'))
            continue
        index = file.find('.MTS')
        if index != -1:
            os.remove(os.path.join(dir_path, file))

if __name__ == "__main__":
    path = input('please input dir path:')
    merge_videos(path)
