import pickle
typesOfMime = [
    ['jpeg','image/jpeg'], 
    ['jpg','image/jpeg'],
    ['png','image/jpeg'],
    ['pdf','application/pdf'],
    ['ppt','application/vnd.ms-powerpoint'],
    ['pptx', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'],
    ['doc', 'application/msword'],
    ['docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    ['txt', 'text/plain']
]

# Run this code to apply the MIME types 
# with open('./DriveOprtn/MIMETypes.mtypd', 'wb') as file:
#     pickle.dump(typesOfMime, file)

# Run the below to check whether the MIME types have successfully been saved or not.
# with open('./DriveOprtn/MIMETypes.mtypd', 'rb') as f:
#     var = pickle.load(f)
# for el in var:
#     print(el, end='\n')


# link for mode MIME types:-
# https://learndataanalysis.org/commonly-used-mime-types/