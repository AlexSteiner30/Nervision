import torch.nn.functional as F
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv1d(768, 768, 1, bias=False),
            nn.Conv1d(768, 512, 1, bias=False),
           
            nn.Conv1d(512, 512, 1, bias=False),
            nn.LeakyReLU(negative_slope=0.2),
            nn.Conv1d(512, 1024, 1, bias=False),
            nn.LeakyReLU(negative_slope=0.2),
            nn.Conv1d(1024, 2048, 1, bias=False),
            nn.LeakyReLU(negative_slope=0.2),
            nn.Conv1d(2048, 2048*3, 1, bias=False),
        )

    def forward(self, input):       
        input = input.reshape(1,512,1)
        x = self.main(input).reshape(2048,3)  

        return x
    
class Discriminator(nn.Module):
    def __init__(self, features=[3, 64, 128, 256, 512, 1024]):
        self.batch_size = 1
        self.layer_num = len(features)-1
        super(Discriminator, self).__init__()

        self.fc_layers = nn.ModuleList([])
        for inx in range(self.layer_num):
            self.fc_layers.append(nn.Conv1d(features[inx], features[inx+1], kernel_size=1, stride=1))

        self.leaky_relu = nn.LeakyReLU(negative_slope=0.2)
        self.final_layer = nn.Sequential(nn.Linear(features[-1], features[-3]),
                                         nn.Linear(features[-3], features[-5]),
                                         nn.Linear(features[-5], 1))

    def forward(self, f):
        feat = f.transpose(1,2)
        vertex_num = feat.size(2)

        for inx in range(self.layer_num):
            feat = self.fc_layers[inx](feat)
            feat = self.leaky_relu(feat)

        out = F.max_pool1d(input=feat, kernel_size=vertex_num).squeeze(-1)
        out = self.final_layer(out) 

        return out