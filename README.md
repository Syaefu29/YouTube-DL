# Youtube-DL
Simple Python script to download Youtube videos.

Based on Shell script guide from Dr. Mark Humphrys:
http://computing.dcu.ie/~humphrys/Notes/UNIX/lab.youtube.html

ITAG values via Fred C. Macall's YTCrack:
http://users.ohiohills.com/fmacall/ytcrack.txt

# How to Use
Invoke from command line, passing a Youtube URL (required) and an ITAG quality flag (optional), for example:
> python youtubedl.py https://www.youtube.com/watch?v=vzp8AE8gEfA

or if you want to specify an ITAG value:
> python youtubedl.py https://www.youtube.com/watch?v=vzp8AE8gEfA 22

# ITAG Values
Please refer to Fred C. Macall's YTCrack documentation for a table of possible ITAG values (http://users.ohiohills.com/fmacall/ytcrack.txt). By default, low quality .FLV will be downloaded.
