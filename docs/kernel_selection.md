import os
import json
from jupyter_client.kernelspec import find_kernel_specs

def find_home_kernels():
    """
    Find all kernels in the home directory and combine them with standard kernels.
    
    Returns:
        dict: A dictionary where keys are kernel names and values are paths to kernel specs.
    """
    # Get standard kernels
    kernels = find_kernel_specs()
    
    # Search for kernels in home directory
    home = os.path.expanduser("~")
    
    for root, dirs, files in os.walk(home):
        if "kernel.json" in files:
            kernel_json_path = os.path.join(root, "kernel.json")
            try:
                with open(kernel_json_path, 'r') as f:
                    kernel_json = json.load(f)
                
                display_name = kernel_json.get('display_name', os.path.basename(root))
                
                # Create a unique name for the kernel
                relative_path = os.path.relpath(root, home)
                kernel_name = f"home-{relative_path.replace(os.path.sep, '-')}"
                
                # Add the kernel to our dictionary
                kernels[kernel_name] = root
                
                print(f"Found kernel: {display_name} at {root}")
            except json.JSONDecodeError:
                print(f"Error reading kernel.json at {kernel_json_path}")
            except Exception as e:
                print(f"Error processing kernel at {root}: {str(e)}")
    
    return kernels

# Example usage
if __name__ == "__main__":
kernels = find_home_kernels()
print("\nAll available kernels:")
for name, path in kernels.items():
    print(f"  {name}: {path}")