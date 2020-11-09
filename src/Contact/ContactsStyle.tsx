import {StyleSheet} from 'react-native';

const styles = StyleSheet.create({
    container:{
	margin: 0,
	marginBottom: 0,
	padding: 10,
        display:'flex',
        backgroundColor:'white',
        flex:1,
	flexDirection: 'column',
    },
    contactLabel:{
	textAlign: 'center',
	fontSize: 35
    },  
    avatarStyle:{
	height: 50,
	width: 50,
    },
    rowContainer: {
	alignItems: 'center',
	display: 'flex',
	flexDirection: 'row',
    }
})

export default styles
