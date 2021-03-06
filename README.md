TopoDelProp is a tool for managing geographic data and metadata of property demarcations

The system maintains five layers of spatial data:

	Land registry units: MultiPolygon layer with perimeters defining properties
	Boundaries: LineString layer with independent property boundaries
	Boundary images: Point layer with the images of the singular points of each boundary
	Interior Elements: MultiPolygon layer with relevant items within the property, such as buildings, swimming pools, ...
	Easements: MultiPolygon layer with easements having the property, such as passing, views, ...

The database has some automatic procedures that prevent entering topologically wrong geometries, as boundaries, easements or interior elements outside the perimeter of the parcel, or boundary images outside the boundary to which they belong.

For a detailed explanation visit http://riunet.upv.es/handle/10251/321/browse?authority=27239&type=author
Visit the geoportal http://upvusig.car.upv.es/geodelprop/, and click in any element.

The sistem uses: Qgis 2.x., PostgreSQL and PostGIS, and Python 2.7

Folder content description:

* databaseSqlCode
Sql code to create new databases in other SRCs diferent of Spain. It creates tables, relations, field indexes, PL/PGsql and trigger functions. TopoDelProp plugin does not work with a database. Create a database with this code is a very complicate process. I am working to improve this. I can create your database and send you a database backup, ready for restore in PostGis. If you are interested in this please contact me (gaspar.mora.navarro@gmail.com).

* pyUPVBibQgis218Plugin
Plugin to facilitate the PostgreSQL operations. Necessary to install it in order TopoDelProp plugin works. It contains classes and methods to connect, insert, delete and update operations. There is an HTML to show the classes documentation.

* TopoDelPropQgis218Plugin
Plugin to manage the geographic data and metadata of topographic properties delimitations

* userManagement
A Python 2.7 utility to manage TopoDelProp users. It allows create, delete enable and disable users.

Links to videos in a poor English explaining the TopoDelProp tool

en_1_geographic_metadata_problem_description https://media.upv.es/player/?id=78b13f40-df4c-11e7-8db7-6f5581cc323c

en_2_topodelprop_system_description https://media.upv.es/player/?id=8dce1010-df4c-11e7-8db7-6f5581cc323c

en_3_topodelprop_query_data https://media.upv.es/player/?id=162cd710-df4e-11e7-8db7-6f5581cc323c

en_4_introduce_data https://media.upv.es/player/?id=a1820210-df4c-11e7-8db7-6f5581cc323c

en_5_detailed_data_introduction_1 https://media.upv.es/player/?id=636b47f0-e183-11e7-8ad7-3f920f6a7e6f

en_5_detailed_data_introduction_2 https://media.upv.es/player/?id=ca1e1030-e184-11e7-8ad7-3f920f6a7e6f

en_5_detailed_data_introduction_3 https://media.upv.es/player/?id=ce29df00-e185-11e7-8ad7-3f920f6a7e6f

en_6_topology_explanation https://media.upv.es/player/?id=f0446190-e186-11e7-8ad7-3f920f6a7e6f

en_7_geoportal_geodelprop https://media.upv.es/player/?id=b371d5e0-df4c-11e7-8db7-6f5581cc323c

Spanish

es_1_descripcion_problema_metadatos https://media.upv.es/player/?id=c3e1e780-df4c-11e7-8db7-6f5581cc323c

es_2_descripcion_sistema_todelprop https://media.upv.es/player/?id=d90b6280-df4c-11e7-8db7-6f5581cc323c

es_3_consulta_con_topodelprop https://media.upv.es/player/?id=eca87120-df4c-11e7-8db7-6f5581cc323c

es_4_introducir_datos https://media.upv.es/player/?id=fb52ddf0-df4c-11e7-8db7-6f5581cc323c

es_5_introducir_datos_detallado_1 https://media.upv.es/player/?id=00dd0270-e18a-11e7-8ad7-3f920f6a7e6f

es_5_introducir_datos_detallado_2 https://media.upv.es/player/?id=bc4ce830-e18b-11e7-8ad7-3f920f6a7e6f

es_6_explicacion_topologia https://media.upv.es/player/?id=04e84a20-e18d-11e7-8ad7-3f920f6a7e6f

es_7_geoportal_geodelprop https://media.upv.es/player/?id=0f8c53a0-df4d-11e7-8db7-6f5581cc323c
