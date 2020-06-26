# import torch
# from torchvision import models
# import torchvision
# from collections import OrderedDict
# import json
# from torch import nn
# import numpy as np 
# from PIL import Image
# from torch.autograd import Variable
import os
import tensorflow as tf
import numpy as np
import PIL


class MLModel:
    # @classmethod
    # def load_checkpoint(cls, filepath):
    #     checkpoint = torch.load(filepath, map_location=torch.device('cpu'))
    #     model = models.resnet152()
    #     # Our input_size matches the in_features of pretrained model
    #     input_size = 2048
    #     output_size = 39
    #     classifier = nn.Sequential(OrderedDict([
    #                         ('fc1', nn.Linear(input_size, 512)),
    #                         ('relu', nn.ReLU()),
    #                         ('fc2', nn.Linear(512, output_size)),
    #                         ('output', nn.LogSoftmax(dim=1))
    #                         ]))
    #     # Replacing the pretrained model classifier with our classifier
    #     model.fc = classifier
    #     model.load_state_dict(checkpoint['state_dict']) 
    #     return model, checkpoint['class_to_idx']

    # @classmethod
    # def process_image(cls, image):
    #     ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
    #         returns an Numpy array
    #     '''
        
    #     # Process a PIL image for use in a PyTorch model

    #     size = 224, 224
    #     image.thumbnail(size, Image.ANTIALIAS)
    #     image = image.crop((128 - 112, 128 - 112, 128 + 112, 128 + 112))
    #     npImage = np.array(image)
    #     npImage = npImage/255.
            
    #     imgA = npImage[:,:,0]
    #     imgB = npImage[:,:,1]
    #     imgC = npImage[:,:,2]
        
    #     imgA = (imgA - 0.485)/(0.229) 
    #     imgB = (imgB - 0.456)/(0.224)
    #     imgC = (imgC - 0.406)/(0.225)
            
    #     npImage[:,:,0] = imgA
    #     npImage[:,:,1] = imgB
    #     npImage[:,:,2] = imgC
        
    #     npImage = np.transpose(npImage, (2,0,1))
        
    #     return npImage


    # @classmethod
    # def predict(cls, image_path, topk=5):
    #     ''' Predict the class (or classes) of an image using a trained deep learning model.
    #     '''
        
    #     # Implement the code to predict the class from an image file
    #     paths = os.path.abspath("libs/plant_disease_classifier.pth")
    #     loaded_model, class_to_idx = cls.load_checkpoint(paths)
    #     idx_to_class = {v : k for k,v in class_to_idx.items()}
    #     image = torch.FloatTensor([cls.process_image(Image.open(image_path))])
    #     loaded_model.eval()
    #     output = loaded_model.forward(Variable(image))
    #     pobabilities = torch.exp(output).data.numpy()[0]
        

    #     top_idx = np.argsort(pobabilities)[-topk:][::-1] 
    #     top_class = [idx_to_class[x] for x in top_idx]
    #     top_probability = pobabilities[top_idx]

    #     return top_probability, top_class

    @classmethod
    def predict(cls, image_path):
        # img = np.array(PIL.Image.open(image_path).resize((224,224))).astype(np.float32)
        paths = os.path.abspath("libs/model.tflite")
        interpreter = tf.lite.Interpreter(model_path=paths)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # input_shape = input_details[0]['shape']
        data = np.array(PIL.Image.open(image_path).resize((224,224))).astype(np.float32)
        data = data / 255.
        data = data.reshape(1, 224, 224, 3)
        interpreter.set_tensor(input_details[0]['index'], data)
        interpreter.invoke()
    
        output_data = interpreter.get_tensor(output_details[0]['index'])
        return output_data