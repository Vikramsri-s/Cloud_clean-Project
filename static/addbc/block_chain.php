<?php


//class Blockchain()
//{
$key="xyz123";



	function addBlock($bc,$bid,$pre,$data,$dtime)
	{
	$fn=$bc."_data.json";
	$hash=md5($data);
	//$hash=encryptIt( $data );
		if($bid=="1")
		{
		$response = array("block_id"=>$bid,"pre_hash"=>$pre,"hash"=>$hash,"date"=>$dtime);
		$res[]=$response;
		$fp = fopen("data/".$fn, 'w');
		fwrite($fp, json_encode($res));
		fclose($fp);
		
		include("dbconnect.php");
		$mq=mysqli_query($connect,"select max(id) from disk_chain_hash");
		$mr=mysqli_fetch_array($mq);
		$id=$mr['max(id)']+1;
		
		mysqli_query($connect,"insert into disk_chain_hash(id,bcode,hdata,vdata) values($id,'$bc','$hash','$data')");
		
		
		}
		else
		{
		$response = array("block_id"=>$bid,"pre_hash"=>$pre,"hash"=>$hash,"date"=>$dtime);
		$inp = file_get_contents("data/".$fn);
		$tempArray = json_decode($inp);
		array_push($tempArray, $response);
		$jsonData = json_encode($tempArray);
		
		file_put_contents("data/".$fn, $jsonData);
		
		include("dbconnect.php");
		$mq=mysqli_query($connect,"select max(id) from disk_chain_hash");
		$mr=mysqli_fetch_array($mq);
		$id=$mr['max(id)']+1;
		
		mysqli_query($connect,"insert into disk_chain_hash(id,bcode,hdata,vdata) values($id,'$bc','$hash','$data')");
		//file_put_contents("data/test.json", $jsonData);
		}
	
	}
	

/*function encryptIt( $q ) {
    $cryptKey  = $key;
    $qEncoded      = base64_encode( mcrypt_encrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), $q, MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ) );
    return( $qEncoded );
}

function decryptIt( $q ) {
    $cryptKey  = $key;
    $qDecoded      = rtrim( mcrypt_decrypt( MCRYPT_RIJNDAEL_256, md5( $cryptKey ), base64_decode( $q ), MCRYPT_MODE_CBC, md5( md5( $cryptKey ) ) ), "\0");
    return( $qDecoded );
}*/



	/*function getBlock($bc,$data)
	{
	$fn=$bc."_data.json";
	$json = file_get_contents("data/".$fn);
	  
	// Decode the JSON file
	$json_data = json_decode($json,true);
	  
	// Display data
	//print_r($json_data);
		
	}*/
//}
?>