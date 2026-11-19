from pathlib import Path
import json, shutil, os
root=Path(r'C:\Users\GonziChan\Desktop\Proyecto_Prode')
p=root/'.active-orchestrator-state.json'
old=json.loads(p.read_text(encoding='utf-8-sig'))
state=json.loads(json.dumps(old,ensure_ascii=False)); d=state['discovery']
backup=root/'tmp/discovery/r1'; backup.mkdir(parents=True,exist_ok=True)
if not (backup/(p.name+'.bak')).exists(): shutil.copy2(p,backup/(p.name+'.bak'))
d['revision']=2; d['updated_on']='2026-11-18'; d['update_authorized_by']='user'
d['update_scope']='Ampliación de despliegue, producción, mantenimiento y aprendizaje; acceso del MVP sólo Google mediante Supabase Auth.'
d['autenticacion']={'status':'approved','approved_on':'2026-11-18','approved_by':'user','provider':'Supabase Auth','mvp_methods':['Google'],'password_prode':False,'out_of_mvp':['Registro por correo/contraseña de PRODE','Recuperación de contraseña propia de PRODE','Otros métodos de acceso'],'responsabilidades_fastapi':['Validar identidad/sesión','Autorizar por pertenencia y rol','Aplicar cierre de pronósticos y permisos administrativos'],'pendiente':['Google y callbacks por entorno','Validación, renovación y revocación de sesión','Identificador estable verificado y perfil PRODE','Soporte ante pérdida de acceso'],'database_provider_adopted':False}
d['despliegue']={'status':'options_evaluated','verified_on':'2026-11-18','guide':'discovery/despliegue-y-aprendizaje.md','routes':['Frontend separado de API y PostgreSQL','React servido por FastAPI y PostgreSQL externo'],'candidates':{'frontend':['Cloudflare Pages'],'api':['Render Free'],'postgresql':['Neon Free','Supabase PostgreSQL Free']},'sqlite':'Alternativa evaluada para un servicio con disco persistente; no adoptada. PostgreSQL sigue aprobado.','pending':['Proveedores y regiones','Despliegue conjunto o separado','DNS','Programación de recordatorios','Cuotas, copias y recuperación']}
d['funcionalidades_necesarias']=[x.replace('Cuentas y permisos, con mecanismo de autenticación pendiente','Acceso sólo Google mediante Supabase Auth; permisos de negocio en FastAPI') for x in d['funcionalidades_necesarias']]
d['integraciones']=[x.replace('Autenticación y correo transaccional por definir','Supabase Auth aprobado con Google como único acceso; sin correo/contraseña propio del MVP. Detalles de sesión y otros correos por justificar.') for x in d['integraciones']]
d['preguntas_abiertas']=[x.replace('Proveedores gratuitos, autenticación, ORM, migraciones y tareas programadas','Proveedores/regiones web/API/PostgreSQL, ORM, migraciones y tareas; Google vía Supabase Auth ya aprobado') for x in d['preguntas_abiertas']]
for key,value in [('reglas_de_negocio','Acceso del MVP únicamente por Google mediante Supabase Auth; sin contraseña propia de PRODE. FastAPI valida identidad y autoriza operaciones.'),('preguntas_abiertas','Configuración Google/callbacks y ciclo seguro de sesión en FastAPI; identidad estable, perfil y soporte ante pérdida de acceso.'),('restricciones','Supabase Auth con Google es el único acceso del MVP; no adopta automáticamente proveedor PostgreSQL ni alojamiento.'),('riesgos','Identidad no verificada o confusión entre autenticación y permisos; participante sin acceso a Google.')]:
 if value not in d[key]: d[key].append(value)
d['casos_de_uso'].insert(0,'Entrar con cuenta Google mediante Supabase Auth sin contraseña adicional de PRODE')
d['mantenimiento']['aprendizaje']=['Fundamentos web MDN','Publicación Vite','Despliegue FastAPI','PostgreSQL respaldo y restauración','CI/CD Full Stack Open','Contenedores Docker','Publicación móvil cuando corresponda']
d['technical_sources']=['https://supabase.com/docs/guides/auth/social-sign-in/auth-google','https://developers.google.com/identity/gsi/web/guides/verify-google-id-token','https://supabase.com/docs/guides/auth/auth-smtp','https://developers.cloudflare.com/pages/platform/limits/','https://render.com/docs/free','https://neon.com/pricing','https://supabase.com/pricing','https://www.sqlite.org/whentouse.html','https://docs.railway.com/pricing/free-trial#data-retention','https://fullstackopen.com/es/part11/introduccion_a_ci_cd/']
assert {k:v for k,v in state.items() if k!='discovery'}=={k:v for k,v in old.items() if k!='discovery'}
assert d['approved_on']=='2026-11-17' and state['step']=='discovery' and state['version']==5
q=p.with_name(p.name+'.r2.tmp'); q.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); os.replace(q,p)
check=json.loads(p.read_text(encoding='utf-8'))
assert {k:v for k,v in check.items() if k!='discovery'}=={k:v for k,v in old.items() if k!='discovery'}
assert check['discovery']['autenticacion']['mvp_methods']==['Google']
g=root/'discovery/despliegue-y-aprendizaje.md'
if not (backup/(g.name+'.bak')).exists(): shutil.copy2(g,backup/(g.name+'.bak'))
t=g.read_text(encoding='utf-8-sig')
anchor='**Relación con Discovery:** complementa el Discovery aprobado el 17 de noviembre; no modifica sus decisiones ni afirma que la aplicación esté desplegada.'
note='**Decisión vigente, 18/11/2026:** el Discovery revisión 2 aprueba Supabase Auth con Google como único acceso del MVP. No hay correo/contraseña propio de PRODE. Los detalles técnicos de sesión siguen pendientes; los proveedores de alojamiento y PostgreSQL no quedan adoptados. Las comparaciones siguientes conservan su contexto histórico y deben leerse con esa decisión.'
if note not in t:
 assert anchor in t
 t=t.replace(anchor,anchor+'\n\n'+note,1)
t=t.replace('**Estado:** anexo educativo y propuesta de recorrido; proveedores todavía no elegidos.','**Estado:** anexo educativo; proveedores de alojamiento/base todavía no elegidos. Autenticación decidida en Discovery revisión 2.')
t=t.replace('Si también queremos comparar autenticación y otros componentes gestionados, Supabase merece una evaluación conjunta.','Supabase Auth ya fue elegido para Google; su PostgreSQL y otros componentes se evaluarán por separado.')
t=t.replace('Elegir proveedor de base no decide automáticamente cómo autenticaremos a los usuarios.','Elegir proveedor de base no modifica la decisión de acceso Google mediante Supabase Auth.')
t=t.replace('La autenticación sigue pendiente de elección.','La decisión vigente es sólo Google mediante Supabase Auth. El correo/contraseña se compara como evolución, no como requisito del MVP.')
t=t.replace('Si se eligiera Supabase Auth, también habría que configurar el envío de correos de confirmación y recuperación para destinatarios reales;', 'Si en una evolución se habilitan flujos por correo en Supabase Auth, habría que configurar su envío para destinatarios reales;')
t=t.replace('Identidad propia o gestionada, con permisos de negocio verificados en FastAPI.','Detalles de integración de Google/Supabase Auth y sesión, con permisos de negocio verificados en FastAPI.')
q=g.with_name(g.name+'.r2.tmp'); q.write_text(t,encoding='utf-8'); os.replace(q,g)
print(json.dumps({'revision':check['discovery']['revision'],'approved_original':check['discovery']['approved_on'],'updated':check['discovery']['updated_on'],'step':check['step'],'only_discovery_changed':True,'auth':check['discovery']['autenticacion'],'guide_coherence_note':note in g.read_text(encoding='utf-8'),'backup_dir':str(backup)},ensure_ascii=False,indent=2))