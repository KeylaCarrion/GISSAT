import sys
from qgis._core import QgsProcessing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication, QgsProcessingFeedback, QgsVectorLayer, QgsProject

QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis-ltr', True)
qgs = QgsApplication([], True)
qgs.initQgis()
sys.path.append(r'C:\OSGeo4W64\apps\qgis-ltr\python\plugins')

import processing
from processing.core.Processing import Processing

Processing.initialize()

QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
feedback = QgsProcessingFeedback()


def algorith_calculate(input_data):
    print(input_data)

    capa1 = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Manzanas_ejemplo.shp'
    capa2 = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poligonos_de_ejemplo.shp'
    output = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada_Zona_Sector.shp'
    output_suma = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada_Zona_Sector_Suma.shp'

    feedback = QgsProcessingFeedback()

    outputs = {}
    results = {}

    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'AreaTotal',
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': 0,  # Coma flotante
        'FORMULA': '$area',
        'INPUT': capa1,
        'NEW_FIELD': True,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }

    outputs['CapaAreaTotal'] = processing.run('qgis:fieldcalculator', alg_params, feedback=feedback)

    insersetion = processing.run('native:intersection', {
        'INPUT': outputs['CapaAreaTotal']['OUTPUT'],
        'OVERLAY': capa2,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }, feedback=feedback)['OUTPUT']

    # Capa de Areas Parciales
    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'PoblacionC',
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': 0,  # Coma flotante
        'FORMULA': ' round("POBTOT"*($area/"AreaTotal"))',
        'INPUT': insersetion,
        'NEW_FIELD': True,
        'OUTPUT': output
    }
    outputs['Poblacion_Calculada'] = processing.run('qgis:fieldcalculator', alg_params, feedback=feedback)

    layer = QgsVectorLayer(output, "Poblacion Calculada", "ogr")
    layout = QgsProject.instance().addMapLayer(layer)
    print(layout.name())

    # Cálculo de la población total
    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': 'Poblacion',
        'FIELD_PRECISION': 0,
        'FIELD_TYPE': 1,  # Entero
        'FORMULA': f'aggregate(layer:=\'{layout.name()}\', '
                   'aggregate:=\'sum\', '
                   'expression:="PoblacionC", '
                   'filter:= "nombre" = attribute(@parent, \'nombre\'))',
        'INPUT': output,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['ClculoDeLaPoblacinTotal'] = processing.run('native:fieldcalculator', alg_params,
                                                        feedback=feedback)
    # Unir atributos por localización
    alg_params = {
        'DISCARD_NONMATCHING': False,
        'INPUT': capa2,
        'JOIN': outputs['ClculoDeLaPoblacinTotal']['OUTPUT'],
        'JOIN_FIELDS': [''],
        'METHOD': 1,  # Tomar solo los atributos del primer objeto coincidente (uno a uno)
        'PREDICATE': [0],  # interseca
        'PREFIX': '',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    }
    outputs['UnirAtributosPorLocalizacin'] = processing.run('native:joinattributesbylocation', alg_params,
                                                            feedback=feedback)
    # Conservar campos
    alg_params = {
        'FIELDS': ['id', 'nombre', 'Poblacion'],
        'INPUT': outputs['UnirAtributosPorLocalizacin']['OUTPUT'],
        'OUTPUT': output_suma
    }
    outputs['ConservarCampos'] = processing.run('native:retainfields', alg_params, feedback=feedback)

    lay = QgsVectorLayer(r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada_Zona_Sector.shp')
    QgsProject.instance().addMapLayer(lay)
    resultado_output = output

    return resultado_output



# Deserializar los datos de entrada
input_data = sys.argv[1]
print("---",input_data)
algorith_calculate(input_data)

qgs.exitQgis()
