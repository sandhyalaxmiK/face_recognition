import face_recognition
import sys,os
import re,cv2
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

input_dir_path=sys.argv[1]
output_dir_path=sys.argv[2]
if not os.path.exists(output_dir_path):
	os.mkdir(output_dir_path)
if not os.path.exists(output_dir_path+'/'+str(1)):
	os.mkdir(output_dir_path+'/'+str(1))
input_images=sorted_alphanumeric(os.listdir(input_dir_path))
cv2.imwrite(output_dir_path+'/'+str(1)+'/'+input_images[0],cv2.imread(input_dir_path+'/'+input_images[0]))
if not os.path.exists(output_dir_path+'/back_imgs'):
	os.mkdir(output_dir_path+'/back_imgs')
if not os.path.exists(output_dir_path+'/error'):
	os.mkdir(output_dir_path+'/error')
		
for img_path in input_images[1:]:
	try:
	
		prev_similarity=0
		img=face_recognition.load_image_file(input_dir_path+'/'+img_path)
		img_encoding=face_recognition.face_encodings(img)
		if img_encoding==[]:
			img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
			cv2.imwrite(output_dir_path+'/back_imgs/'+img_path,img)
			continue
		img_encoding=face_recognition.face_encodings(img)[0]	
		imgs_dirs=sorted_alphanumeric(os.listdir(output_dir_path))
		imgs_dirs=list(set(imgs_dirs)-set(['error','back_imgs']))
		for img_dir in imgs_dirs:
	
			check_img=face_recognition.load_image_file(output_dir_path+'/'+img_dir+'/'+sorted_alphanumeric(os.listdir(output_dir_path+'/'+img_dir))[0])
			check_img_encoding=face_recognition.face_encodings(check_img)[0]
			similarity=1-face_recognition.compare_faces([img_encoding], check_img_encoding)
		
			if similarity>prev_similarity:
				prev_similarity=similarity
				result_dir=img_dir
		img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
		if prev_similarity<0.6:
				new_dir=str(len(os.listdir(output_dir_path))+1)
				os.mkdir(output_dir_path+'/'+new_dir)
				cv2.imwrite(output_dir_path+'/'+new_dir+'/'+img_path,img)
		else:
			cv2.imwrite(output_dir_path+'/'+result_dir+'/'+img_path,img)
	except:
		img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
		cv2.imwrite(output_dir_path+'/error/'+img_path,img)
