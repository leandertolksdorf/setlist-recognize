import os
import tempfile
import subprocess

class Slicer():
    def __init__(self, mp3_file, temp_path):
        super().__init__()
        self.mp3_file = mp3_file
        self.temp_path = temp_path
        self.density = 60 # seconds
        self.length = 20 # seconds

        '''
        density =   180     | 120   | 60    | 60    | 60    | 120   | 90    | 75    | 75
        length =    10      | 10    | 15    | 10    | 5     | 5     | 5     | 5     | 10
        time        1:11    | 1:55  | 3:39  | 3:29  | 3:23  | 1:47  | 2:20  | 2:48  | 2:42
        tracks      14      | 16    | 20    | 20    | 20    | 16    | 18    | 19    | 19
        '''

    def set_density(self,density):
        self.density = density

    def set_length(self,length):
        self.length = length

    def make_samples(self):

        # Make folders

        os.mkdir('{}/samples'.format(self.temp_path))

        # Slice mp3 into segments of set density. Save slices in temporary directory.

        slices = tempfile.TemporaryDirectory(dir = self.temp_path)

        subprocess.run(['ffmpeg', '-i',str(self.mp3_file), '-f','segment', '-segment_time', str(self.density), '-c', 'copy', '{}/slice_%03d.mp3'.format(slices.name)])

        # Trim slices to set length.

        sample_number = 0

        for filename in os.listdir("{}".format(slices.name)):
            subprocess.run(['ffmpeg','-i','{}/{}'.format(slices.name,filename),'-ss','0','-to',str(self.length),'-c','copy','-y','{}/samples/sample_{}.mp3'.format(self.temp_path,sample_number)])

            sample_number += 1