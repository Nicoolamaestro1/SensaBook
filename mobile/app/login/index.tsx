import { View } from "react-native";
import { Text, TextInput, Button } from "react-native";

export default function LoginScreen() {
  return (
    <View className="container d-flex justify-content-center align-items-center vh-100">
      <View className="card p-4 shadow" style={{ width: 350 }}>
        <Text className="h4 mb-3">Login</Text>
        <TextInput placeholder="Email" className="form-control mb-2" />
        <TextInput placeholder="Password" secureTextEntry className="form-control mb-3" />
        <Button title="Login" />
      </View>
    </View>
  );
}
