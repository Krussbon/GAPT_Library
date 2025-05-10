import random

def generate_academic_title():
    modifiers = [
        "A Study on", "Exploring", "Investigating", "An Analysis of",
        "The Role of", "Revisiting", "The Impact of", "Understanding",
        "A Comparative Study of", "An Interdisciplinary Approach to"
    ]

    topics = [
        # Physics
        "Quantum Entanglement", "Dark Matter", "String Theory", "Gravitational Waves",
        "Particle Acceleration", "Thermodynamics", "Quantum Tunneling",

        # Biology
        "Gene Expression", "Microbiome Diversity", "CRISPR-Cas9 Systems", 
        "Protein Folding", "Cellular Aging", "Evolutionary Biology",

        # Psychology
        "Cognitive Bias", "Behavioral Conditioning", "Memory Retention", 
        "Social Anxiety", "Dream Analysis", "Emotional Regulation",

        # Humanities
        "Postcolonial Literature", "Philosophy of Language", 
        "Ethical Dilemmas in AI", "Sociopolitical Discourse", "Gender Theory",
        "Classical Rhetoric", "Narrative Identity",

        # Interdisciplinary
        "Neural Networks", "Artificial Intelligence", "Digital Humanities",
        "Cultural Impacts of Technology", "Science Communication"
    ]

    contexts = [
        "in Contemporary Society", "in the 21st Century", "through a Historical Lens",
        "among Adolescents", "in Higher Education", "using Computational Models",
        "across Disciplines", "in Clinical Practice", "in Literature and Art",
        "with Quantum Computing", "in Modern Research", "using fMRI"
    ]

    return f"{random.choice(modifiers)} {random.choice(topics)} {random.choice(contexts)}"

# Generate examples
for _ in range(5):
    print(generate_academic_title())
