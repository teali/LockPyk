<html>
	<head>
		<title>TNP-iframe-test</title>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
		<style>
			p{
				font-family:arial;
				padding:0;
				margin:0;
				color:rgb(0,33,85);
			}
			iframe{
				border:none;
				position:absolute;
			}
			.header{
				position:absolute;
				background-color: #fff;
				z-index:1;
				width:1200px;
				height:55px;
			}
			.header #title{
				float:left;
				
				padding-left:30px;
				padding-top:10px;				
				
				font-size: 2em;
			}
			.tabs{
				padding-left:100px;
				float:left;
			}
			.tabs div{
				-webkit-touch-callout: none;
				-webkit-user-select: none;
				-khtml-user-select: none;
				-moz-user-select: none;
				-ms-user-select: none;
				user-select: none;
				float:left;
				margin-left:20px;
				cursor:pointer;
			}
			.tabs div p:hover{
				background-color:rgb(0,99,255);
			}
			.tabs div p{
				padding-left:15px;
				padding-right:15px;
				margin-top:10px;
				font-size:1em;
				text-align: center;
				line-height:40px;
			}
		</style>
	</head>
	<body>
		<div class="header">
			<p id="title">EPortal</p>
			<div class="tabs">
				<div id="view" onclick="view()">
					<p>View</p>
				</div>
				<div id="customer" onclick="customer()">
					<p>Customer</p>
				</div>
				<div id="circuit" onclick="circuit()">
					<p>Circuit</p>
				</div>
			</div>
		</div>
		<iframe src="http://artemis:8015/tnp/index.jsp#LUIopen/customer/1" height="800" width="1200" id="tnp" ></iframe>
		<script type="text/javascript">
			function view(){
				document.getElementById('tnp').src = "http://artemis:8015/tnp/index.jsp#LUIsearch/view/.exe=f"
			}
			function customer(){
				document.getElementById('tnp').src = "http://artemis:8015/tnp/index.jsp#LUIsearch/customer/.exe=f"
			}
			function circuit(){
				document.getElementById('tnp').src = "http://artemis:8015/tnp/index.jsp#LUIsearch/path/.exe=f"
			}
			$(function(){
				$.ajax({
				  url: "http://artemis:8015/tnp/login/j_security_check",
				 data: "j_username=admin&j_password=admin"
				  });
			});
		</script>
	</body>

</html>
