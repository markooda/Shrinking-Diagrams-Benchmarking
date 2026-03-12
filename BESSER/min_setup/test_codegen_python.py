import os
from besser.generators.python_classes import PythonGenerator
from besser.BUML.metamodel.structural import (
    Class,
    DomainModel,
    Enumeration,
    EnumerationLiteral,
    DateType,
    StringType,
    IntegerType,
    Property,
    BinaryAssociation,
    Multiplicity,
)

from besser.BUML.metamodel.structural import DomainModel
from besser.BUML.notations.structuralPlantUML import plantuml_to_buml

model_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(model_dir, "test.plantuml")
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path=model_path)


def test_generator(domain_model):
    # Create an instance of the generator
    output_dir = "output"
    generator = PythonGenerator(model=domain_model, output_dir=str(output_dir))

    # Generate Python classes
    generator.generate()

    # Check if the file was created
    output_file = os.path.join(str(output_dir), "classes.py")

    # Read the generated file
    with open(output_file, "r", encoding="utf-8") as f:
        generated_code = f.read()


test_generator(modeltest)
