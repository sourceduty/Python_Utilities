import tkinter as tk
from tkinter import ttk
import numpy as np

# Step 1: Neuron Implementation
class SimpleNeuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def process_input(self, text):
        # Example: using the length of the text as input feature
        input_feature = len(text)
        weighted_sum = self.weights * input_feature + self.bias
        return self.sigmoid(weighted_sum)

# Step 2: GUI Implementation
class NeuronApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Neuron Text Processor")

        self.neuron = SimpleNeuron(weights=0.1, bias=0.0)
        
        self.label = ttk.Label(root, text="Enter Text:")
        self.label.pack(pady=10)
        
        self.text_entry = ttk.Entry(root, width=50)
        self.text_entry.pack(pady=10)
        
        self.result_label = ttk.Label(root, text="Neuron Output: ")
        self.result_label.pack(pady=10)
        
        self.process_button = ttk.Button(root, text="Process", command=self.process_text)
        self.process_button.pack(pady=10)

    def process_text(self):
        text = self.text_entry.get()
        output = self.neuron.process_input(text)
        self.result_label.config(text=f"Neuron Output: {output:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuronApp(root)
    root.mainloop()
