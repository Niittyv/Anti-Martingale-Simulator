import simulator
import analyzer

if __name__ == '__main__':
    
    metadata, result = simulator.simulator()
    
    generate_report = ""
    while generate_report not in ["y", "n"]:
        generate_report = input("want to generate html-report? (y/n) " ).lower()
        
    if generate_report == "y":
        analyzer.generate_report(result, metadata)