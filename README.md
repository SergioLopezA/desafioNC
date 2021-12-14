complementos instalados:
  * django
  * pillow
  * pythton-barcode

El proyecto lo probé con Postman y lo hice en puro Django.

los servicios los direccione con los urls localhost:8000/tax/unpaid/ para generar y listar las facturas con la posiblidad de filtrar por tipo de servicio completando en el url 
/?service=<y el nombre del seevicio>
y localhost:8000/tax/transaction/ para las transacciones tambien podiendo filtrar por un rango de fecha tambien completando el url /?f_date=<9999-99-99>&e_date<9999-99-99>
  
Tuve un problema en la creacion de las transacciones y todavia no he logrado dar con el error, siento que debido adentrarme con el rest-framework pero por inexperiencia
quise probar este camino.
  
 Agradezco cualquier observacion o comentario.
  
  Gracias!!
