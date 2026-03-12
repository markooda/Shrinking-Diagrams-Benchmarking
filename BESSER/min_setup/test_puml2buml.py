import os
from besser.BUML.metamodel.structural import DomainModel
from besser.BUML.notations.structuralPlantUML import plantuml_to_buml

model_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(model_dir, "test.plantuml")
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path=model_path)

classes = modeltest.classes_sorted_by_inheritance()

for cls in classes:
    print(cls.name)
