<?php
session_start();
include("dbconnect.php");
extract($_REQUEST);
include("block_chain.php");

$rdate=date("d-m-Y");
$ch1=mktime(date('H')+5,date('i')+30,date('s'));
$rtime=date('H:i:s',$ch1);


$dtime=$rdate.", ".$rtime;

$key="xyz123";

$qq4=mysqli_query($connect,"select * from disk_chain where bcode='$bc'");
$rr4=mysqli_fetch_array($qq4);
$bcount=$rr4['block_count'];
$bid=$bcount+1;
if($bcount>0)
{
$pre=$rr4['pre_value'];
#$dtt=$data.", ".$dtime;
#$pre1=md5($dtt);
$dtt=md5($data);
//$dtt=encryptIt( $data );
$pre1=$dtt;
}
else
{
$pre="00000000000000000000000000000000";
//$dtt=$data.", ".$dtime;
$dtt=md5($data);
//$dtt=encryptIt( $data );
$pre1=$dtt;
}



$sq1=mysqli_query($connect,"select * from disk_chain where bcode='$bc'");
$sn1=mysqli_num_rows($sq1);
if($sn1==0)
{
$mq=mysqli_query($connect,"select max(id) from disk_chain");
$mr=mysqli_fetch_array($mq);
$id=$mr['max(id)']+1;
mysqli_query($connect,"insert into disk_chain(id,block_count,pre_value,bcode,rdate) values($id,'$bid','$pre1','$bc','$rdate')");
}
else
{

mysqli_query($connect,"update disk_chain set block_count=$bid,pre_value='$pre1' where bcode='$bc'");
}


addBlock($bc,$bid,$pre,$data,$dtime);


?>