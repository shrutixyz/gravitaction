import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { Button, StyleSheet, Text, View, Alert} from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={{color: '#333333',fontSize: 40, fontStyle: 'italic',
    fontWeight: "bold", alignSelf: 'flex-start', margin: 30}}>Walkation</Text>

<Design/>

      
      <Button title="show me around" onPress={() => Alert.alert('welcome to walkation')} color="purple" />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E0BBE4',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
});



const Design = ()=>{
return (
<View style={{ flexDirection: "row"}} > 
<View style={{backgroundColor: 'violet', height: 10, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'indigo', height: 20, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'blue', height: 30, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'green', height: 40, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'yellow', height: 50, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'orange', height: 60, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'red', height: 70, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'violet', height: 80, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'indigo', height: 90, width: 40,opacity: 0.4}} > 

</View>
<View style={{backgroundColor: 'blue', height: 100, width: 40, opacity: 0.4}} > 

</View>
</View>
);
}