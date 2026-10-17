import com.comsol.model.*;
import com.comsol.model.util.ModelUtil;
import java.util.*;

/** Public-source-only reconstruction. No legacy MPH is an input. */
public class Ma2019Cross {
 static String ROOT;
 static ArrayList<double[]> outline(String shape){
  double L=shape.equals("S2")?16:9;
  double[]cs=shape.equals("S2")?new double[]{3,6.5,10,13.5}:new double[]{4.5};
  ArrayList<double[]>p=new ArrayList<>();p.add(new double[]{-.5,0});p.add(new double[]{.5,0});
  for(double y:cs){p.add(new double[]{.5,y-.5});p.add(new double[]{4,y-.5});p.add(new double[]{4,y+.5});p.add(new double[]{.5,y+.5});}
  p.add(new double[]{.5,L});p.add(new double[]{-.5,L});
  for(int i=cs.length-1;i>=0;i--){double y=cs[i];p.add(new double[]{-.5,y+.5});p.add(new double[]{-4,y+.5});p.add(new double[]{-4,y-.5});p.add(new double[]{-.5,y-.5});}
  return p;
 }
 static ArrayList<double[]> edges(String s){
  var p=outline(s);ArrayList<double[]>out=new ArrayList<>();
  for(int i=0;i<p.size();i++){double[]a=p.get(i),b=p.get((i+1)%p.size());
   // S0/S1 identical mask excludes ALL four candidate contact faces, regardless of BC.
   boolean exclude=(a[1]==0&&b[1]==0)||(a[0]==b[0]&&Math.abs(a[0])==4)||(!s.equals("S2")&&a[1]==9&&b[1]==9);
   if(!exclude)out.add(new double[]{a[0],a[1],b[0],b[1]});
  }return out;
 }
 static String f(double d){return String.format(Locale.US,"%.13g",d);}
 static String um(double d){return f(d)+"[um]";}
 static void polygon(GeomSequence g,String tag,ArrayList<double[]> p){
  g.create(tag,"Polygon");g.feature(tag).set("source","table");String[][]v=new String[p.size()][2];
  for(int i=0;i<p.size();i++){v[i][0]=f(p.get(i)[0]);v[i][1]=f(p.get(i)[1]);}g.feature(tag).set("table",v);
 }
 static void box(Model m,String tag,double x0,double x1,double y0,double y1){
  m.component("c").selection().create(tag,"Box");var s=m.component("c").selection(tag);s.geom("g",1);s.set("condition","inside");
  s.set("xmin",um(x0-1e-7));s.set("xmax",um(x1+1e-7));s.set("ymin",um(y0-1e-7));s.set("ymax",um(y1+1e-7));
 }
 static void terminal(Model m,String tag,String sel,boolean floating){
  m.component("c").physics("ec").create(tag,"Terminal",1);var t=m.component("c").physics("ec").feature(tag);t.selection().named(sel);
  t.set("TerminalType",floating?"Current":"Voltage");t.set(floating?"I0":"V0",floating?"0[A]":"0[V]");
 }
 static String minn(List<String> v){String s=v.get(0);for(int i=1;i<v.size();i++)s="min("+s+","+v.get(i)+")";return s;}
 static Model build(String shape,double width,double he,double thickness)throws Exception{
  Model m=ModelUtil.create("M");m.modelPath(ROOT+"/models");
  m.param().set("g_sheet","1e-4[S]");m.param().set("d_eff",f(thickness)+"[nm]");
  m.param().set("q0","0.01[A/m]");m.param().set("w","0.5[um]");m.param().set("t_edge",um(width));
  m.param().set("h_edge",um(he));m.param().set("x0","0[um]");m.param().set("y0","4.5[um]");
  m.param().set("source_on","0");m.param().set("source_case","2");m.param().set("targetV","1[V]");
  m.component().create("c",true);m.component("c").geom().create("g",2);GeomSequence g=m.component("c").geom("g");g.lengthUnit("um");
  polygon(g,"sample_bulk",outline(shape));polygon(g,"sample_edge",outline(shape));
  var es=edges(shape);ArrayList<String>caps=new ArrayList<>();HashSet<String>vertices=new HashSet<>();int k=0;
  for(double[]e:es){
   String r="strip"+k;g.create(r,"Rectangle");
   if(e[1]==e[3]){g.feature(r).set("pos",new String[]{f(Math.min(e[0],e[2])),f(e[1])+"-t_edge/1[um]"});g.feature(r).set("size",new String[]{f(Math.abs(e[2]-e[0])),"2*t_edge/1[um]"});}
   else{g.feature(r).set("pos",new String[]{f(e[0])+"-t_edge/1[um]",f(Math.min(e[1],e[3]))});g.feature(r).set("size",new String[]{"2*t_edge/1[um]",f(Math.abs(e[3]-e[1]))});}
   caps.add(r);
   for(int j=0;j<2;j++){double x=e[2*j],y=e[2*j+1];String key=x+","+y;
    if(vertices.add(key)){String c="disk"+k+"_"+j;g.create(c,"Circle");g.feature(c).set("pos",new double[]{x,y});g.feature(c).set("r","t_edge/1[um]");caps.add(c);}
   }k++;
  }
  g.create("caps","Union");g.feature("caps").selection("input").set(caps.toArray(new String[0]));g.feature("caps").set("intbnd",false);
  g.create("bulk","Difference");g.feature("bulk").selection("input").set("sample_bulk");g.feature("bulk").selection("input2").set("caps");g.feature("bulk").set("keepsubtract",true);g.feature("bulk").set("selresult",true);
  g.create("collar","Intersection");g.feature("collar").selection("input").set(new String[]{"sample_edge","caps"});g.feature("collar").set("intbnd",false);g.feature("collar").set("selresult",true);
  g.run();
  // All domains belong to the continuous semiconductor, collar only partitions mesh/integration.
  m.component("c").selection().create("all_dom","Explicit");m.component("c").selection("all_dom").geom("g",2);m.component("c").selection("all_dom").all();
  int[]collar=m.component("c").selection("g_collar_dom").entities();
  m.component("c").selection().create("edge_dom","Explicit");m.component("c").selection("edge_dom").geom("g",2);m.component("c").selection("edge_dom").set(collar);
  box(m,"bottom",-.5,.5,0,0);double L=shape.equals("S2")?16:9;box(m,"top",-.5,.5,L,L);
  double[]cs=shape.equals("S2")?new double[]{3,6.5,10,13.5}:new double[]{4.5};
  for(int i=0;i<cs.length;i++){box(m,"left"+i,-4,-4,cs[i]-.5,cs[i]+.5);box(m,"right"+i,4,4,cs[i]-.5,cs[i]+.5);}
  m.component("c").variable().create("vars");Expr v=m.component("c").variable("vars");v.selection().named("all_dom");
  ArrayList<String>ds=new ArrayList<>();ArrayList<String>nsx=new ArrayList<>(),nsy=new ArrayList<>(),near=new ArrayList<>();k=0;
  for(double[]e:es){double dx=e[2]-e[0],dy=e[3]-e[1],len=Math.hypot(dx,dy);String id="e"+k;
   v.set(id+"u","min(1,max(0,((x-"+um(e[0])+")*"+um(dx)+"+(y-"+um(e[1])+")*"+um(dy)+")/("+um(len)+")^2))");
   v.set(id+"px",um(e[0])+"+"+um(dx)+"*"+id+"u");v.set(id+"py",um(e[1])+"+"+um(dy)+"*"+id+"u");
   v.set(id+"d","sqrt((x-"+id+"px)^2+(y-"+id+"py)^2)");ds.add(id+"d");
   v.set(id+"nx","if("+id+"d<1e-9[um],"+f(dy/len)+",-(x-"+id+"px)/max("+id+"d,1e-9[um]))");
   v.set(id+"ny","if("+id+"d<1e-9[um],"+f(-dx/len)+",-(y-"+id+"py)/max("+id+"d,1e-9[um]))");
   String close="if("+id+"d<=edge_d+1e-9[um],1,0)";near.add(close);nsx.add("("+close+")*"+id+"nx");nsy.add("("+close+")*"+id+"ny");k++;
  }
  v.set("edge_d",minn(ds));v.set("edge_mask","if(edge_d<=t_edge,1,0)");v.set("nxsum",String.join("+",nsx));v.set("nysum",String.join("+",nsy));
  v.set("normsum","sqrt(nxsum^2+nysum^2)");v.set("nedge_x","nxsum/max(normsum,1e-14)");v.set("nedge_y","nysum/max(normsum,1e-14)");
  v.set("G","exp(-2*((x-x0)^2+(y-y0)^2)/w^2)");
  v.set("qsx","source_on*q0*G*if(source_case<0.5,1/sqrt(2),if(source_case<1.5,edge_mask/sqrt(2),edge_mask*nedge_x))");
  v.set("qsy","source_on*q0*G*if(source_case<0.5,1/sqrt(2),if(source_case<1.5,edge_mask/sqrt(2),edge_mask*nedge_y))");
  m.component("c").physics().create("ec","ConductiveMedia","g");var ec=m.component("c").physics("ec");ec.selection().named("all_dom");
  System.out.println("EC_PROPS,"+Arrays.toString(ec.prop().tags())+",FEATURES,"+Arrays.toString(ec.feature().tags()));
  ec.prop("d").set("d","d_eff");ec.feature("cucns1").set("sigma_mat","userdef");ec.feature("cucns1").set("sigma",new String[][]{{"g_sheet/d_eff"},{"0"},{"0"},{"0"},{"g_sheet/d_eff"},{"0"},{"0"},{"0"},{"g_sheet/d_eff"}});
  terminal(m,"target","bottom",false);ec.feature("target").set("V0","targetV");
  if(shape.equals("S0"))terminal(m,"ground_top","top",false);
  else for(int i=0;i<cs.length;i++){boolean floating=shape.equals("S2")&&i<cs.length-1;terminal(m,"t_left"+i,"left"+i,floating);terminal(m,"t_right"+i,"right"+i,floating);}
  ec.create("src","ExternalCurrentDensity",2);ec.feature("src").selection().named("all_dom");ec.feature("src").set("Je",new String[][]{{"qsx/d_eff"},{"qsy/d_eff"},{"0"}});
  m.component("c").mesh().create("mesh","g");var mesh=m.component("c").mesh("mesh");mesh.feature("size").set("custom","on");mesh.feature("size").set("hmax","0.15[um]");mesh.feature("size").set("hmin","0.004[um]");
  mesh.create("edge_size","Size");mesh.feature("edge_size").selection().named("edge_dom");mesh.feature("edge_size").set("custom","on");mesh.feature("edge_size").set("hmax","h_edge");mesh.feature("edge_size").set("hmin","h_edge/3");
  ArrayList<Integer>ce=new ArrayList<>();for(String sel:m.component("c").selection().tags())if(sel.equals("bottom")||sel.equals("top")||sel.startsWith("left")||sel.startsWith("right"))for(int b:m.component("c").selection(sel).entities())ce.add(b);
  mesh.create("contact_size","Size");mesh.feature("contact_size").selection().geom("g",1);mesh.feature("contact_size").selection().set(ce.stream().mapToInt(i->i).toArray());mesh.feature("contact_size").set("custom","on");mesh.feature("contact_size").set("hmax","h_edge");mesh.feature("contact_size").set("hmin","h_edge/3");
  mesh.create("tri","FreeTri");mesh.run();
  m.study().create("std");m.study("std").create("stat","Stationary");
  System.out.println("AUDIT,"+shape+",domains="+Arrays.toString(m.component("c").selection("all_dom").entities())+",collar="+Arrays.toString(collar)+",mesh="+mesh.getNumElem()+",width_um="+width+",h_um="+he+",d_nm="+thickness);
  for(String s:m.component("c").selection().tags())try{System.out.println("SELECTION,"+s+","+Arrays.toString(m.component("c").selection(s).entities()));}catch(Exception e){}
  System.out.println("NATIVE_D,"+ec.prop("d").getString("d"));System.out.flush();return m;
 }
 static void solve(Model m,String label,boolean first){long t=System.nanoTime();if(first)m.study("std").run();else m.sol("sol1").runAll();System.out.printf(Locale.US,"SOLVED,%s,%.6f%n",label,(System.nanoTime()-t)*1e-9);System.out.flush();}
 static void numerics(Model m){
  for(String tag:new String[]{"int_all","int_edge"}){m.result().numerical().create(tag,"IntSurface");m.result().numerical(tag).set("data","dset1");m.result().numerical(tag).selection().named(tag.equals("int_all")?"all_dom":"edge_dom");m.result().numerical(tag).set("intorder",6);}
  m.result().numerical().create("terms","EvalGlobal");m.result().numerical("terms").set("data","dset1");
 }
 static double[] vals(Model m,String tag){double[][]a=m.result().numerical(tag).getReal();double[]o=new double[a.length];for(int i=0;i<a.length;i++){o[i]=a[i][0];if(!Double.isFinite(o[i]))throw new IllegalStateException("nonfinite "+tag);}return o;}
 static String G(double x,double y){return "exp(-2*((x-"+um(x)+")^2+(y-"+um(y)+")^2)/w^2)";}
 static double[] kernel(Model m,double x,double y,int order){
  String z="q0*"+G(x,y),kx="*d(V,x)/1[V]",ky="*d(V,y)/1[V]";
  var a=m.result().numerical("int_all");a.set("intorder",order);a.set("expr",new String[]{z+kx,z+ky});double[]b=vals(m,"int_all");
  var e=m.result().numerical("int_edge");e.set("intorder",order);e.set("expr",new String[]{z+kx,z+ky,z+"*(nedge_x*d(V,x)+nedge_y*d(V,y))/1[V]"});double[]q=vals(m,"int_edge");
  return new double[]{(b[0]+b[1])/Math.sqrt(2),(q[0]+q[1])/Math.sqrt(2),q[2],q[0],q[1]};
 }
 static void emitK(String label,double x,double y,double[]k){System.out.printf(Locale.US,"K,%s,%.8f,%.8f",label,x,y);for(double z:k)System.out.printf(Locale.US,",%.16e",z);System.out.println();System.out.flush();}
 static ArrayList<String> terms(Model m){ArrayList<String>t=new ArrayList<>();for(String f:m.component("c").physics("ec").feature().tags())if(m.component("c").physics("ec").feature(f).getType().equals("Terminal"))t.add(f);return t;}
 static void direct(Model m,String label,int sc,double x,double y,double predicted)throws Exception{
  m.param().set("x0",um(x));m.param().set("y0",um(y));m.param().set("source_case",Integer.toString(sc));m.param().set("source_on","1");m.param().set("targetV","0[V]");solve(m,label+"_direct",false);
  var tags=terms(m);ArrayList<String>ex=new ArrayList<>();for(int i=1;i<=tags.size();i++)ex.add("ec.I0_"+i);for(int i=1;i<=tags.size();i++)ex.add("ec.V0_"+i);
  m.result().numerical("terms").set("expr",ex.toArray(new String[0]));double[]v=vals(m,"terms");
  // Independently integrate actual J, not the prescribed I0 constraint. n is outward from sheet.
  for(int i=0;i<tags.size();i++){
   String n="flux"+i;
   if(!Arrays.asList(m.result().numerical().tags()).contains(n)){m.result().numerical().create(n,"IntLine");m.result().numerical(n).set("data","dset1");m.result().numerical(n).selection().set(m.component("c").physics("ec").feature(tags.get(i)).selection().entities());}
   m.result().numerical(n).set("intorder",8);m.result().numerical(n).set("expr",new String[]{"(-g_sheet*mean(d(V,x))+mean(qsx))*nx+(-g_sheet*mean(d(V,y))+mean(qsy))*ny"});
  }
  double[]fl=new double[tags.size()];for(int i=0;i<fl.length;i++)fl[i]=vals(m,"flux"+i)[0];
  System.out.printf(Locale.US,"D,%s,%d,%.8f,%.8f,%.16e",label,sc,x,y,predicted);
  for(double z:v)System.out.printf(Locale.US,",%.16e",z);for(double z:fl)System.out.printf(Locale.US,",%.16e",z);System.out.println();System.out.flush();
 }
 static double[][] probes(String s){return s.equals("S2")?new double[][]{{-.35,2.35},{.35,2.35},{-.35,7.15},{.35,7.15},{-.35,9.35},{.35,9.35},{-.35,14.15},{.35,14.15}}:new double[][]{{-.35,3.85},{.35,3.85},{-.35,5.15},{.35,5.15},{0,4.5},{.35,6.5}};}
 /** Execute one independently rebuilt example; never loads an existing model. */
 public static void execute(String shape,String output,boolean smoke)throws Exception{
  if(!Arrays.asList("S0","S1","S2").contains(shape))throw new IllegalArgumentException("Unknown geometry: "+shape);
  // Python prepares the new destination. Use only COMSOL's model/export APIs
  // for file output, without requesting Java filesystem permission changes.
  ROOT=output;
  ModelUtil.showProgress(false);Model m=null;String label=shape+"_public";
  try{
   m=build(shape,0.1,0.02,1);solve(m,label+"_weight",true);numerics(m);
   double[][]all=probes(shape),ps=smoke?new double[][]{all[0],all[2]}:all;
   double[][]ks=new double[ps.length][];
   for(int i=0;i<ps.length;i++){
    ks[i]=kernel(m,ps[i][0],ps[i][1],6);emitK(label,ps[i][0],ps[i][1],ks[i]);
    double[]q=kernel(m,ps[i][0],ps[i][1],10);
    System.out.printf(Locale.US,"ORDER,%s,%d",label,i);
    for(int j=0;j<q.length;j++)System.out.printf(Locale.US,",%.16e",q[j]-ks[i][j]);
    System.out.println();
   }
   // The scan is integrated on the finite-element mesh of the auxiliary solution.
   // Smoke mode is four isolated sample positions, not a resolved spatial map.
   if(smoke){
    for(double[]p:ps)for(double x:new double[]{-0.35,0.35})emitK(shape+"_map",x,p[1],kernel(m,x,p[1],6));
   }else{
    int ny=shape.equals("S2")?86:51;
    for(int iy=0;iy<ny;iy++)for(int ix=0;ix<46;ix++){
     double x=-4.5+0.2*ix,y=-0.5+0.2*iy;emitK(shape+"_map",x,y,kernel(m,x,y,6));
    }
   }
   fieldExport(m,shape);
   m.save(ROOT+"/models/"+shape+"_weighting.mph");
   // Check the edge-normal source only; all three source kernels are exported above.
   for(int i=0;i<ps.length;i++)direct(m,label,2,ps[i][0],ps[i][1],ks[i][2]);
   System.out.println("COMPLETE,"+label);System.out.flush();
  }finally{if(m!=null)ModelUtil.remove("M");}
 }
 static boolean inside(ArrayList<double[]>p,double x,double y){
  boolean in=false;for(int i=0,j=p.size()-1;i<p.size();j=i++){
   double[]a=p.get(i),b=p.get(j);if((a[1]>y)!=(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])in=!in;
  }return in;
 }
 static void fieldExport(Model m,String shape){
  var poly=outline(shape);int ny=shape.equals("S2")?160:90;ArrayList<String>xs=new ArrayList<>(),ys=new ArrayList<>();
  for(int iy=0;iy<ny;iy++)for(int ix=0;ix<80;ix++){double x=-3.95+.1*ix,y=.05+.1*iy;if(inside(poly,x,y)){xs.add(um(x));ys.add(um(y));}}
  m.result().dataset().create("field_points","CutPoint2D");m.result().dataset("field_points").set("data","dset1");m.result().dataset("field_points").set("pointx",xs.toArray(new String[0]));m.result().dataset("field_points").set("pointy",ys.toArray(new String[0]));
  m.result().export().create("field_export","Data");m.result().export("field_export").set("data","field_points");
  m.result().export("field_export").set("expr",new String[]{"x/1[um]","y/1[um]","V/1[V]","d(V,x)/1[V]","d(V,y)/1[V]","nedge_x","nedge_y","edge_mask"});
  m.result().export("field_export").set("filename",ROOT+"/data/"+shape+"_fields_COMSOL.csv");m.result().export("field_export").run();System.out.println("FIELD_EXPORT,"+shape+",points="+xs.size());
 }
}
