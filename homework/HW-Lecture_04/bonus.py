# Goal: write 3 modules; tokenizer, MoE, and simple neural network to assist with coding.



import re  
import torch
import torch.nn as nn
import torch.nn.functional as F


class Tokenizer:
    def __init__(self):
        # Using a regular expression to handle complex tokenization
        self.token_pattern = re.compile(r"\w+|[^\w\s]")

    def tokenize(self, text):
        # Tokenize the text using the compiled regular expression
        tokens = self.token_pattern.findall(text)
        return tokens

class MoE(nn.Module):
    def __init__(self, num_experts, input_size, output_size):
        super(MoE, self).__init__()
        self.num_experts = num_experts
        self.experts = nn.ModuleList([nn.Linear(input_size, output_size) for _ in range(num_experts)])
        self.gate = nn.Linear(input_size, num_experts)

    def forward(self, x):
        # Gating mechanism: Get weights for each expert
        gates = F.softmax(self.gate(x), dim=1)
        
        # Output from each expert
        expert_outputs = [expert(x) for expert in self.experts]
        
        # Combine expert outputs weighted by the gating mechanism
        expert_outputs = torch.stack(expert_outputs, dim=1)  # Shape: (batch_size, num_experts, output_size)
        output = torch.sum(gates.unsqueeze(-1) * expert_outputs, dim=1)
        
        return output

# Example usage
input_size = 10
output_size = 5
num_experts = 3
model = MoE(num_experts, input_size, output_size)

# Example input
x = torch.randn(1, input_size)  # Batch size of 1
output = model(x)
print(output)

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Define layers of the neural network
        self.layer1 = nn.Linear(in_features=10, out_features=20)  # Example layer
        self.layer2 = nn.Linear(in_features=20, out_features=5)   # Output layer

    def forward(self, x):
        # Forward pass through the network
        x = F.relu(self.layer1(x))  # Activation function applied after first layer
        x = self.layer2(x)          # Output layer (no activation here, assuming regression or raw output needed)
        return x

# Example usage
# Initialize the neural network
model = SimpleNN()

# Create some example input data (e.g., a batch of 3 samples, each with 10 features)
x = torch.randn(3, 10)

# Forward pass through the network to get the output
output = model(x)
print(output)


  
# Usage
tokenizer = Tokenizer()
moe = MoE()
simple_nn = SimpleNN()

text = "Hello, world!"
tokens = tokenizer.tokenize(text)
moe_output = moe.forward(tokens)
nn_output = simple_nn.forward(moe_output)
print(nn_output)

