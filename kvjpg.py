import piexif
import datetime
import glob
import sys
import os
import re

# global variables
AppVersion = '1.06'

debug = False

cntstrfmt = 'CNT%04d0-'
datestrfmt = '%Y-%m-%d-'

cntstrre = re.compile('CNT(\d+)-')
datestrre = re.compile('(\d\d\d\d-\d\d-\d\d)-')

defaultdatetime = datetime.datetime.strptime('1901:01:01 00:00:01', '%Y:%m:%d %H:%M:%S')

# take the string that was passed in on the command line and make needed variables
#
# timedeltastr format:re.compile_string:offset_seconds_int:range1_int:range2_int_optional
#  re.compile_string - string passed into the re.compile command - used to determine if a filename matches
#                      this should extract the picture number associated with pictures that match
#  offset_seconds_int - int number of seconds to change the time on photos that match
#  range1_int - int starting number of photo file that matches the RE
#  range2_int - int (optional) ending number of phone file that matches the RE
#
def parse_optiondict_timedelta( timedeltastr, debug=False ):
    (compile_str,offset_sec,*range_str) = timedeltastr.split(':')
    re_compile=re.compile(compile_str)
    timedelta=int(offset_sec)
    # debugging
    if debug:
        print('range_str:',range_str)
        print('range_str[0]:', range_str[0])
        print('len:', len(range_str))
    # parse up what was passed in
    if len(range_str)==2:
        pic_range=range(int(range_str[0]),int(range_str[1]))
    else:
        pic_range=int(range_str[0])
    return(re_compile,timedelta,pic_range)

# routine to pull the date from the filename rather than from the file
def parse_date_from_filename( filename, debug=False ):
    # perform matching on filename
    m = re.search(datestrre, filename)
    s = re.search(cntstrre, filename)
    # debug
    if debug:
        print('filename:',filename)
        print('m',m)
        if m:  print('m.group0:' ,m.group(0))
        if m:  print('m.group1:' ,m.group(1))
        print('s',s)
        if s:  print('s.group0:', s.group(0))
        if s:  print('s.group1:', s.group(1))

    # check for match on date in filename
    if m:
        # check for match on count in filename
        if s:
            # we are using filename date and cnt to build the time
            return datetime.datetime.strptime(m.group(1), '%Y-%m-%d') + datetime.timedelta(seconds=int(s.group(1)))
        else:
            # we are using justfilename date to build the time
            return datetime.datetime.strptime(m.group(1), '%Y-%m-%d')
    else:
        # we are using the default date to build the time
        return defaultdatetime
    
# bust up the filename and strip previously implemented strings in the basename
def parse_cleanup_filename( filename, debug=False ):
    # split the filename up
    (dirname, basename) = os.path.split(filename)
    if debug:
        print('parse_cleanup_filename:dirname:', dirname)
        print('parse_cleanup_filename:basename:', basename)
    # make dirname normal path
    dirname = os.path.normpath(dirname)
    # remove CNT in the basename string if it exists
    basename = re.sub( cntstrre, '', basename )
    if debug:  print('parse_cleanup_filename:basename-post-cnt:', basename)
    # remove DATESTR in the basename string if it exists
    basename = re.sub( datestrre, '', basename )
    if debug:  print('parse_cleanup_filename:basename-post-date:', basename)
    # return results
    return ( dirname, basename )

# 
# offset the datetime in filename_row[0] by timedelta_offset if the filename in filename_row[1] re.search matches re_filename
#   filename_row = 2 position list [ datetime, filename_str ]
#   re_filename = re.compile() that extracts out the image number (eg. re.compile('IMG_(\d).JPG', re.IGNORECASE))
#   timedelta_offset = datetime.timedelta object (eg. datetime.timedelta(seconds=-30*60) - 30 minute earlier)
#   filerange = int or range of int that defines the re.compile matching values that we apply offset to (eg. 3466 or range(3455,3470)
#
# this routine can be used when two cameras don't have the same date/time in them.  using this will move the time
# date of one cameras picture to align with the timedate of the other camera
#
def datetime_offset_for_matching_filename( filename_row, re_filename, timedelta_offset, filerange, debug=False ):
    if debug:
        print('datetime_offset_for_matching_filename:filename_row:', filename_row)
        print('datetime_offset_for_matching_filename:re_filename:', re_filename)
        print('datetime_offset_for_matching_filename:timedelta_offset:', timedelta_offset)
        print('datetime_offset_for_matching_filename:filerange:', filerange)
        print('datetime_offset_for_matching_filename:filename_row[1]:', filename_row[1])
    m = re.search( re_filename, filename_row[1] )
    if m:
        picture = int(m.group(1))
        if debug:
            print('datetime_offset_for_matching_filename:filename-match: true')
            print('datetime_offset_for_matching_filename:picture:', picture)
            print('datetime_offset_for_matching_filename:filename_row[0]-before:', filename_row[0])
            
        if picture == filerange or picture in filerange:
            # filename match - change the timedate record by offset
            filename_row[0] += timedelta_offset
            if debug:
                print('datetime_offset_for_matching_filename:filename_row[0]-after:', filename_row[0])
                
        
# display all exif attributes for the file passed in
def display_exif_attributes( filename, debug=False ):
    exif_dict = piexif.load( filename )
    print('ifds:', exif_dict.keys())
    print('ifd : tag : name : value')
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            print(ifd, ':', tag, ':', piexif.TAGS[ifd][tag]["name"], ':', exif_dict[ifd][tag])

    
# default:  get the DateTime out of JPG meta data
def get_exif_attribute_from_jpg( fn, ifd='0th', tag=306, debug=False ):
    exif_dict = piexif.load(fn)
    # convert the attributes to a datetime object if its name is datetime
    if 'DateTime' in piexif.TAGS[ifd][tag]["name"]:
        try:
            return datetime.datetime.strptime(exif_dict[ifd][tag].decode("utf-8") , '%Y:%m:%d %H:%M:%S')
        except Exception:
            return datetime.datetime.now()
    # if not converted - return the value
    return exif_dict[ifd][tag]


# process a list of files
#   recount - flag that says we are going to sort using the date in the filename not the date in the file
def get_date_sorted_filelists( fileglob, recount=False, debug=False  ):
    # local variable
    datefilelist = []

    # pull the filelist and sort by filename
    filelist = sorted(glob.glob( fileglob ))

    # step through this list of files - and grab a date associated with each file
    for fname in filelist:
        if recount:
            # the date we use is pulled from the filename
            fdate = parse_date_from_filename( fname )
        elif fname.lower().endswith('.jpg'):
            # add in the ability to pull the adate
        
            # get file date of the picture form meta data
            fdate = get_exif_attribute_from_jpg( fname )
        else:
            # not a jpg - then use a default date/time
            fdate = defaultdatetime

        # add this record to list
        datefilelist.append([fdate, fname])

    # create sorted list
    datefilelistsorted = sorted(datefilelist)

    # return the two lists
    return (filelist, datefilelistsorted)

    
# create list of actions to be taken
def create_file_action_list( datefilelistsorted, copytodir=None, adddate=False, addcnt=True, debug=False ):
    datestr=''
    cntstr=''
    if copytodir:
        actionstr = 'copy'
        copytodir = os.path.normpath(copytodir)
    else:
        actionstr = 'ren'
    filecnt = 0
    actionline = []
    
    # step through the files
    for (fdate, fname) in datefilelistsorted:
        # increment the file counter
        filecnt += 1

        # calc the date string
        if adddate:
            datestr = datetime.datetime.strftime(fdate, datestrfmt)

        # calc the counter string
        if addcnt:
            cntstr = cntstrfmt % filecnt

        # split up the current fname
        (dirname, basename) = parse_cleanup_filename( fname )

        # put it back togehter
        # fname = os.path.join( dirname, basename )

        # make the input filename normal path structure
        fname = os.path.normpath( fname )

        # create the new basename
        basenamenew = ''.join((datestr,cntstr,basename))

        # create the output filename
        if copytodir:
            fnamenew = os.path.join( copytodir, basenamenew )
        else:
            # learning - you DON'T put the path into the new name when renaming
            #fnamenew = os.path.join( dirname, basenamenew )
            fnamenew = basenamenew
            
        # calculate the file string
        actionline.append('%s "%s" "%s"' % (actionstr, fname, fnamenew))

    # when done return the list
    return actionline

# take action list nad write it out of a file
def write_action_list_to_file( filename, actionlist, workingdir=None, debug=False ):
    with open( filename, 'w' ) as out:
        if workingdir:
            out.write('cd "' + workingdir + '"\n')
        out.write('\n'.join(actionlist))

if __name__ == '__main__':
    #filelist = build_bat_reorder_by_datetaken( '*.*' )
    (filelist,sortedfilelist) = get_date_sorted_filelists( '*.*' )
    print('filelist:', filelist)
    print('sortedfilelist:', sortedfilelist)
    save_file_change( sortedfilelist, 'file.bat', True )
    
    jpgdate = get_exif_attribute_from_jpg( "IMG_2666.JPG" )
    print(type(jpgdate))
    print(jpgdate)
    sys.exit()
    

