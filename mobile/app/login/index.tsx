import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";
import { useRouter } from "expo-router";
import { apiService } from "../../services/api";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert("Error", "Please enter both email and password");
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiService.login({ email, password });
      console.log("Login successful:", response);
      router.replace("/library-page");
    } catch (error: any) {
      Alert.alert("Error", `Login failed: ${error?.message || "Unknown error"}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Email"
        placeholderTextColor="#aaa"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor="#aaa"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity
        style={[styles.button, isLoading && { opacity: 0.6 }]}
        onPress={handleLogin}
        disabled={isLoading}
        activeOpacity={0.8}
      >
        <Text style={styles.buttonText}>
          {isLoading ? "Logging in..." : "Login"}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => console.log("Forgot Password pressed")}>
        <Text style={styles.forgotPassword}>Forgot Password?</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 24,
    backgroundColor: "transparent", // 👈 nema backgrounda
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 32,
    color: "#fff", // belo na tamnoj pozadini (ili pozadinskoj slici)
  },
  input: {
    width: "100%",
    maxWidth: 340,
    height: 50,
    borderWidth: 1,
    borderColor: "#B4B4B4",
    borderRadius: 50,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 16,
    color: "#EAEAEA",
    backgroundColor: "transparent",
  },
  button: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "transparent",
    paddingVertical: 14,
    borderWidth: 1,
    borderColor: "#B4B4B4",
    borderRadius: 50,
    marginTop: 8,
    marginBottom: 16,
  },
  buttonText: {
    textAlign: "center",
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  forgotPassword: {
    color: "#ddd",
    fontSize: 14,
  },
});
