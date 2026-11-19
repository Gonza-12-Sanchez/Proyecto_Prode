from pathlib import Path
import shutil, os, re
root=Path(r'C:\Users\GonziChan\Desktop\Proyecto_Prode')
p=root/'discovery/discovery.md'
s=p.read_text(encoding='utf-8-sig')
backup=root/'tmp/discovery/r1'
backup.mkdir(parents=True,exist_ok=True)
if not (backup/'discovery.md.bak').exists(): shutil.copy2(p,backup/'discovery.md.bak')
def rep(old,new):
 global s
 if old not in s: raise RuntimeError('No encontrado: '+old[:90])
 s=s.replace(old,new,1)
rep('**Fecha:** 17 de noviembre de 2026  \n**Revisión:** 1  \n**Estado:** aprobado por el usuario en la conversación de fundación.', '**Fecha original:** 17 de noviembre de 2026  \n**Actualización:** 18 de noviembre de 2026  \n**Revisión:** 2  \n**Estado:** aprobación original del usuario el 17 de noviembre; ampliación y acceso sólo por Google autorizados el 18 de noviembre.')
rep('No están elegidos los proveedores de alojamiento, autenticación, automatización ni la integración de fútbol.', 'Se aprobó Supabase Auth con Google como único acceso del MVP. FastAPI valida la identidad y los permisos de negocio. No están elegidos los proveedores de alojamiento web/API/PostgreSQL, automatización ni datos de fútbol; elegir Supabase Auth no adopta automáticamente su PostgreSQL.')
rep('## 1. Problema que resuelve', '### Alcance de la revisión 2\n\nSe integra la conversación sobre despliegue gratuito, SQLite, producción móvil, mantenimiento y aprendizaje. Se confirma acceso exclusivamente por Google mediante Supabase Auth, sin contraseña propia de PRODE. Las opciones de alojamiento siguen como recomendaciones pendientes; no se afirma que haya infraestructura creada ni código implementado.\n\n## 1. Problema que resuelve')
rep('El mecanismo de autenticación está pendiente.', 'El único acceso del MVP será Google mediante Supabase Auth, sin correo/contraseña propio de PRODE.')
rep('- Planes y suscripciones para el público general.', '- Planes y suscripciones para el público general.\n- Otros métodos de autenticación gestionada si se necesitan después; no integran el acceso del MVP.')
rule='| RN-18 | Único acceso del MVP: cuenta Google mediante Supabase Auth. PRODE conserva perfil y relaciones del juego, no almacena la contraseña Google ni ofrece contraseña propia. FastAPI valida identidad y autoriza cada operación. |\n'
s=s.replace('\n**Ejemplos de puntuación:**', '\n'+rule+'\n**Ejemplos de puntuación:**',1)
rep('Cloudflare Pages, Render y Supabase se discutieron como candidatos', 'Cloudflare Pages, Render, Neon y Supabase PostgreSQL se discutieron como candidatos')
rep('- **Identidad y correos:** autenticación propia o gestionada y correo transaccional por definir. Los permisos de negocio se verifican en un entorno de confianza, no sólo en la pantalla.', '- **Identidad aprobada:** sólo Google mediante Supabase Auth. Detalles técnicos del ciclo de sesión pendientes de arquitectura; FastAPI conserva autorización. Correo/contraseña y recuperación de contraseña propia están fuera del MVP. Otros correos sólo se agregarán si se justifican.')
rep('- La fundación se realiza en la raíz PRODE.', '- La raíz actual es `C:/Users/GonziChan/Desktop/Proyecto_Prode`, tras el traslado indicado por el usuario.')
rep('| Arquitectura/KB | Proveedores gratuitos, autenticación, ORM/migraciones, estrategia de tareas, despliegue conjunto o separado, recuperación y cuotas. |', '| Arquitectura/KB | Proveedores/regiones web/API/PostgreSQL, ORM/migraciones, tareas, despliegue conjunto o separado, recuperación y cuotas. Supabase Auth y acceso sólo Google ya decididos. |\n| Arquitectura/KB | Google/callbacks por entorno, validación/ciclo/revocación de sesión, identidad estable y perfil, soporte ante pérdida de acceso. |')
rep('| Antes del piloto | Tamaño real del grupo, responsable de operación, dedicación, fecha y criterios medibles de validación. |', '| Antes del piloto | Tamaño real del grupo, disponibilidad de cuenta Google, responsable de operación, dedicación, fecha y criterios medibles de validación. |')
rep('| La persona responsable no sabe operar un producto desplegado. | Guía y práctica de despliegue, diagnóstico, reversión y restauración antes de depender del sistema. |', '| La persona responsable no sabe operar un producto desplegado. | Guía y práctica de despliegue, diagnóstico, reversión y restauración antes de depender del sistema. |\n| La identidad se acepta sin verificar o se confunde login con permisos. | Validación de sesión y autorización por operación en FastAPI; no confiar roles/correos del cliente. |\n| Participante sin cuenta Google o que pierde acceso al proveedor. | Confirmar viabilidad del piloto y definir soporte; otros métodos quedan como evolución. |')
append=(root/'tmp/discovery/r2-additions.md').read_text(encoding='utf-8-sig')
for n in range(12,16): assert re.search(r'^## '+str(n)+r'\. ',append,re.M)
rep('## Fuentes y precedencia',append.strip()+'\n\n## Fuentes y precedencia')
rep('La fuente primaria de decisiones es la conversación confirmada por el usuario el 17 de noviembre de 2026.', 'La fuente primaria de decisiones es la conversación aprobada por el usuario el 17 de noviembre y ampliada por su solicitud el 18 de noviembre de 2026, con acceso sólo Google vía Supabase Auth.')
rep('## Continuidad de la fundación', '**Fuentes de la ampliación:** las secciones 12 a 15 enlazan documentación oficial de despliegue, identidad, producción y aprendizaje consultada el 18 de noviembre. Las notas locales `discovery/despliegue-y-aprendizaje.md` y `discovery/sources/despliegue-simple-sqlite.md` conservan la investigación detallada. Los proveedores de alojamiento comparados no se consideran adoptados.\n\n## Continuidad de la fundación')
rep('El PDF solicitado será una presentación de este Discovery, no una certificación de producto implementado ni de fundación completa.', 'El PDF reflejará la revisión 2 de este Discovery, no una certificación de producto implementado ni fundación completa. La aprobación original y su ampliación quedan trazadas; el paso sigue en discovery hasta el checkpoint de avance.')
for n in range(1,16): assert re.search(r'^## '+str(n)+r'\. ',s,re.M)
assert all(f'RN-{n:02d}' in s for n in range(1,19))
assert 'El mecanismo de autenticación está pendiente' not in s
q=p.with_name('discovery.md.r2.tmp'); q.write_text(s.rstrip()+'\n',encoding='utf-8'); os.replace(q,p)
print(str(p));print('Revision2; secciones15; reglas18; lineas',len(s.splitlines()));print('Backup',str(backup/'discovery.md.bak'))