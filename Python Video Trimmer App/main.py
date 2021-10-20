from tkinter import *
from tkinter import messagebox
import easygui
import vlc
import os, time
from sys import exit
import subprocess


DIRECTORY = os.path.dirname(os.path.realpath(os.sys.argv[0]))
print("Dir: {}".format(DIRECTORY))
TRIMMING_DATA_FILE = DIRECTORY + '/_video_trimming_data.txt'
OUTPUTS = DIRECTORY + "/outputs.txt"


def getPaths():
    paths = []

    valid_extensions = ['3g2', '3gp', 'svi', 'm4v', 'mp4', 'mpg', 'm2v', 'mpv', 'mp2', 'mpe', 'm4p', 'amv', 'wmv', 'mov', 'avi', 'ogg', 'ogv', 'mkv']

    for file in os.listdir(DIRECTORY):
        if not file.startswith("scanned_") and (file[-3:] in valid_extensions or file[-4:] == 'mpeg'):
            paths.append(file)

    return paths


class App:


    def __init__(self):
        self.trim_points = []

        # video self.player object
        self.player = None

        # GUI objects
        self.seekbar = None
        self.file_name_label = None
        self.file_size_label = None

        self.cur_video_file = None
        self.videos = None
        self.video_idx = None

        self.root = Tk()


    def storeData(self, file_path):
        # no modifications to be made
        if len(self.trim_points) <= 2:
            print("There were no trimming points set. Skipping to next video.")
            answer = messagebox.askquestion("Mark processed", "Do you want to mark this video as\ndone processing even though no trim points were set?")
            if answer == 'yes':
                new_name = "scanned_" + file_path
                os.rename(file_path, new_name)
            return

        self.trim_points.sort(key=lambda interval: interval[1])

        time_segments = []

        i = 0
        while i < len(self.trim_points):
            cur_segment = [0, 0]
            # find latest starting point possible
            while i < len(self.trim_points) and self.trim_points[i][0] == 'start':
                cur_segment[0] = self.trim_points[i][1]
                i += 1
            # find first and skip rest of ends of segment
            end_start = self.trim_points[i][1]
            cur_segment[1] = end_start
            i += 1
            while i < len(self.trim_points) and self.trim_points[i][0] == 'end':
                i += 1
            time_segments.append(cur_segment)

        if DIRECTORY[1:] in file_path:
            file_path = file_path[len(DIRECTORY) + 1:len(file_path)]  # make sure it is ./file_name
        

        with open(TRIMMING_DATA_FILE, 'a') as out_file:
            final_out_string = file_path + '\n'

            for trim_segment in time_segments:
                final_out_string += str(trim_segment[0]) + '\n'  # add start time in seconds
                final_out_string += str(trim_segment[1]) + '\n'  # add end time of segment

            final_out_string += 'end\n'  # mark end of this video's trimming data

            out_file.write(final_out_string)
            print("Data stored successfully!")


    # constructs a trim point with marks: start or end and with time in
    # seconds, rouneded down from miliseconds
    def constructTrimPoint(self, mark, time_value_ms):  # in miliseconds
        time_in_seconds = time_value_ms // 1000
        return (mark, time_in_seconds)


    # ======================
    # Event listeners:

    # on change event for slider/self.seekbar
    def seekTo(self, dummy):
        # avoid double call when updating self.seekbar
        cur_time = self.player.get_time()
        seek_time = self.seekbar.get() * 1000  # convert to miliseconds
        if abs(cur_time - seek_time) > 2300:  # if difference is larger than 2.3 seconds set video time
            self.player.set_time(seek_time)  # needed to be miliseconds


    def initialiseSeekbar(self):

        if not self.player:
            return

        self.trim_points = [('start', 0), self.constructTrimPoint('end', self.player.get_length())]
        print("Duration of cur video is: " + str(self.trim_points[1][1]) + " seconds")
        if self.seekbar:
            self.seekbar.destroy()
        self.seekbar = Scale(self.root, from_=0, to=self.trim_points[1][1], orient=HORIZONTAL, length=900, command=self.seekTo)
        self.seekbar.place(x=50, y=160)  # need to be packed after creation or it does not work


    def updateSeekbar(self):
        self.seekbar.set((self.player.get_time() // 1000))
        self.root.after(1000, self.updateSeekbar)


    def updateLabels(self):

        if self.file_name_label:
            self.file_name_label.destroy()
        if self.file_size_label:
            self.file_size_label.destroy()

        self.file_name_label = Label(self.root, text=str("File name: " + self.cur_video_file))
        try:
            self.file_size_label = Label(self.root, text=str("Size: " + str(os.path.getsize(self.cur_video_file) // 1000000) + " MB"))
        except:
            pass
        self.file_name_label.place(x=20, y=20)
        self.file_size_label.place(x=20, y=40)


    def playVideo(self):
        self.player.play()


    def pauseVideo(self):
        self.player.pause()


    def closePlayer(self):
        if self.player:
            self.player.stop()


    def openVideoFile(self):
        media = easygui.fileopenbox(title="Choose file to play")
        if not media:
            return
        if DIRECTORY[1:] in media:
            media = media[len(DIRECTORY) + 1:len(media)]

        self.cur_video_file = media

        if self.player:
            self.closePlayer()
        time.sleep(2)
        self.player = vlc.MediaPlayer(str(self.cur_video_file))
        time.sleep(1)
        self.player.set_title = str(self.cur_video_file)
        self.updateLabels()

        time.sleep(1)

        # start new trim points array
        self.trim_points = [('start', 0), self.constructTrimPoint('end', self.player.get_length())]
        print("Initialised an end point to: " + str(self.trim_points[1][1]) + " seconds")

        self.initialiseSeekbar()


    def quitApp(self):
        print("Quit was pressed.")

        # ask if they are sure to quit:
        msg = "Do you really want to exit the app?"
        if len(self.trim_points) > 2:
            msg = """There are videos which were not trimmed yet.
    If you quit the app now, trimming data will not be lost.
    To trim the videos press Initialise Trimming button.
    Are you sure you want to quit?
    """

        answer = messagebox.askquestion("Quit", msg)

        if answer == "yes":
            self.closePlayer()
            time.sleep(2)
            self.root.destroy()
            exit(0)


    def createStartPoint(self):
        self.trim_points.append(self.constructTrimPoint('start', self.player.get_time()))


    def createEndPoint(self):
        self.trim_points.append(self.constructTrimPoint('end', self.player.get_time()))


    def initialiseTrimming(self):
        # check if there is anything to trim
        nothing_to_trim = False
        with open(TRIMMING_DATA_FILE, 'r') as in_file:
            lines = in_file.readlines()
            if len(lines) == 0:
                nothing_to_trim = True

        if nothing_to_trim == True:
            messagebox.showinfo("Important", "There are no videos set to trim.")
            return

        # make buttons unclickable besides Quit  HERE
        self.closePlayer()

        # display message to wait until trimmer is done
        messagebox.showwarning("Info", "Please wait until trimming is done")

        # initialise trimmer
        try:
            subprocess.call('trimmer.exe')
            #os.startfile(str(DIRECTORY + '\\trimmer.exe'))
        except subprocess.CalledProcessError as error:
            print("Trimmer sent an error: " + str(error))
            messagebox.showerror("Error", "An error with the trimmer occured.\nSome of the files failed to be trimmed. Try them again later.")


        # when trimmer is done go through output file,
        # display the new cut version and prompt if they want to delete original
        # if they want to delete trimmed version and mark original scanned or to be scanned again
        # rename the file which was kept, accordingly (with scanned or unscanned tag)

        messagebox.showinfo("Info", "Now each new trimmed file will be played and\n automatically skipping parts for you to check if you are satisfied with it.\nPlease do not click Next Video and Delete this Video buttons since\nthose actions will be handled automatically.")

        with open(OUTPUTS, 'r') as in_file:
            lines = in_file.readlines()
            try:
                for i in range(1, len(lines), 2):
                    msg_save = "Do you want to save this trimmed file?"
                    msg_delete = "Do you want to delete the original file? This is permanent."

                    new_file_name = lines[i].strip()
                    original_file = lines[i - 1].strip()

                    self.player = vlc.MediaPlayer(new_file_name)
                    self.player.set_title = new_file_name

                    if self.file_name_label:
                        self.file_name_label.destroy()
                    if self.file_size_label:
                        self.file_size_label.destroy()

                    self.file_name_label = Label(self.root, text=str("File name: " + new_file_name))
                    self.file_name_label.place(x=20, y=20)
                    self.file_size_label = Label(self.root, text=str("Size: " + str(os.path.getsize(new_file_name) // 1000000) + " MB"))
                    self.file_size_label.place(x=20, y=40)

                    self.player.play()
                    
                    time.sleep(2)
                    self.initialiseSeekbar()

                    i = 1
                    while i <= 4:
                        i += 1
                        self.player.set_time((i * self.player.get_length()) // 5)
                        time.sleep(3)

                    answer = messagebox.askquestion("Save trimmed file", msg_save)
                    if answer == 'yes':
                        self.closePlayer()
                        time.sleep(2)
                        new_name = "scanned_" + new_file_name  # mark that it has been processed
                        os.rename(new_file_name, new_name)

                        answer = messagebox.askquestion("Delete original", msg_delete)
                        if answer == 'yes':
                            os.remove(original_file)  # remove original
                        else:
                            answer = messagebox.askquestion("Mark processed", "Do you want to mark the original video as processed?")
                            if answer == 'yes':
                                new_name = "scanned_" + original_file
                                os.rename(original_file, new_name)
                    else:
                        self.closePlayer()
                        time.sleep(2)
                        os.remove(new_file_name)  # remove trimmed video
                        answer = messagebox.askquestion("Delete original", "Do you want to delete the original file too? (This is permanent)")
                        if answer == 'yes':
                            os.remove(original_file)  # remove original
                        else:
                            answer = messagebox.askquestion("Mark processed", "Do you want to mark the original video as processed?")
                            if answer == 'yes':
                                new_name = "scanned_" + original_file
                                os.rename(original_file, new_name)
            except:
                print("Error occured with opening trimmed files!")

        # clear old trim points:
        with open(TRIMMING_DATA_FILE, 'w') as out_file:
            out_file.write("")

        with open(OUTPUTS, "w") as out_file:
            out_file.write("")

        # once done, unfreeze the buttons HERE

        self.player = vlc.MediaPlayer(self.cur_video_file)
        self.player.set_title = self.cur_video_file
        self.updateLabels()

        self.player.play()

        time.sleep(0.2)
        self.initialiseSeekbar()

        messagebox.showinfo("Done", "Trimming is all done, you can go back to what you were doing now.")


    def nextVideo(self):
        self.closePlayer()
        
        # store this video's trimming data
        print("Storing data")
        self.storeData(self.cur_video_file)

        # update video, play next if any left
        self.video_idx += 1
        if (self.video_idx >= n):        
            messagebox.showinfo(message="All videos have been processed.\nCongratulations!")

            msg = "Do you want to trim previously marked videos now?"
            if len(self.trim_points) > 2:
                answer = messagebox.askquestion("Confirm trimming", msg)
                if answer == "yes":
                    self.initialiseTrimming()

            msg = "Do you want to quit?"
            answer = messagebox.askquestion("Quit", msg)
            if answer == "yes":
                self.closePlayer()
                time.sleep(2)
                self.root.destroy()
                exit(0)
            else:
                return

        self.cur_video_file = self.videos[self.video_idx]
        print("current video: " + str(self.cur_video_file))
        self.player = vlc.MediaPlayer(self.cur_video_file)
        self.player.set_title = self.cur_video_file
        self.updateLabels()

        self.player.play()
        time.sleep(3)

        # start new trim points array
        self.initialiseSeekbar()


    def deleteVideo(self):
        answer = messagebox.askquestion("Delete current video", "Are you sure you want to delete currently played video?")
        if answer == 'no':
            return
        self.closePlayer()
        time.sleep(1)
        os.remove(self.cur_video_file)
        print("Deleted " + str(self.cur_video_file))
        self.nextVideo()



if __name__ == "__main__":
    app = App()
    app.video_idx = 0
    app.videos = getPaths()
    n = len(app.videos)

    # initialise GUI:
    app.root.title("Mass Video Batch Trimmer")
    app.root.geometry("1000x240")

    time.sleep(1)

    # add buttons
    app.file_name_label = Label(app.root, text="")
    app.file_size_label = Label(app.root, text="")
    app.file_name_label.place(x=20, y=20)
    app.file_size_label.place(x=20, y=40)

    Button(app.root, text="Initialise Trimmer", command=app.initialiseTrimming).pack(side=LEFT)
    Button(app.root, text="  Next Video", command=app.nextVideo).pack(side=LEFT)
    Button(app.root, text="  Play  ", command=app.playVideo).pack(side=LEFT)
    Button(app.root, text="  Pause  ", command=app.pauseVideo).pack(side=LEFT)
    Button(app.root, text="Add Start Point ==>", command=app.createStartPoint).pack(side=LEFT)
    Button(app.root, text="<== Add End Point", command=app.createEndPoint).pack(side=LEFT)
    Button(app.root, text="Open Video", command=app.openVideoFile).pack(side=LEFT)
    Button(app.root, text="Close Video", command=app.closePlayer).pack(side=LEFT)
    Button(app.root, text="Delete this Video", command=app.deleteVideo).pack(side=LEFT)
    Button(app.root, text="  Quit   ", command=app.quitApp).pack(side=LEFT)


    if (app.video_idx >= n):
        messagebox.showinfo("Info", "There are no more unprocessed app.videos in this directory\n")
    else:
        # start first video:
        app.cur_video_file = app.videos[app.video_idx]
        print("current video: " + str(app.cur_video_file))

        app.player = vlc.MediaPlayer(app.cur_video_file)
        app.player.set_title = app.cur_video_file
        app.updateLabels()

        app.player.play()

        time.sleep(0.2)

        # update app.seekbar and initialise frist trim points
        app.initialiseSeekbar()  # does both

    # reschedule updating app.seekbar every second
    app.root.after(1000, app.updateSeekbar)
    # run the infinite loop of the app
    app.root.mainloop()
