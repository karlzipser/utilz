from utilz.vis import *
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

def shape_from_tensor(x):
    return shape( x.detach().numpy() )

def cuda_to_rgb_image(cu):
    return z55(cu.detach().cpu().numpy()[0,:].transpose(1,2,0))

#EOF
