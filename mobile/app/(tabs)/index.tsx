
import { Text, View } from "react-native";
import LoginScreen from "../login";

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#E7CC20FF",
      }}
    >
      <Text style={{ color: "white", fontSize: 32, fontWeight: "bold" }}>
        SensaBook
      </Text>

      <LoginScreen />

    </View>
  );
}
