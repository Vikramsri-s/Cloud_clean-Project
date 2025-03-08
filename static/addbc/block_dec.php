<?php
session_start();
include("dbconnect.php");
extract($_REQUEST);

$fp=fopen("key.txt","r");
$key=fread($fp,filesize("key.txt"));
fclose($fp);

?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Health Chain</title>
<style type="text/css">
.bor
{
border-bottom:dotted #999999 1px;
}
</style>
</head>

<body>
<p>&nbsp;</p>
<h3 align="center">Block Information</h3>

<p>&nbsp;</p>
<form name="form1" method="post">
<p align="center">
<input type="password" name="kk" />
<input type="submit" name="btn" value="Decrypt" />
</p>
</form>
<?php

if(isset($btn))
{

	if($kk==$key)
	{

$q1=mysqli_query($connect,"select * from disk_chain_hash");
while($r1=mysqli_fetch_array($q1))
{

$i++;

$ss=explode(",",$r1['vdata']);
$tt=explode(":",$ss[1]);
$uu=$tt[1];

	if($uu==$uname)
	{
													
														
														
	?>
	<table width="100%" cellpadding="5" cellspacing="5">
	<tr>
	<td width="18%" align="left" style="color:#0066FF">Block ID</td>
	<td width="82%" align="left" style="color:#FF33CC">: <?php echo $i; ?></td>
	</tr>
	<tr>
	<td align="left" style="color:#0066FF">Data</td>
	<td align="left" style="color:#FF33CC">: <?php echo $r1['vdata']; ?></td>
	</tr>
	
	
</table>
	<?php
	}
}

	
	}
	else
	{
	?><p align="center" style="color:#FF0000">Wrong Key!</p><?php
	}
}//btn
?>
</body>
</html>
