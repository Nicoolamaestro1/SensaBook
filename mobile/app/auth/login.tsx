import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";
import ScreenBackground from "../components/ScreenBackground";
import { useRouter } from "expo-router";
import { apiService } from "../../services/api";
import Ionicons from "@expo/vector-icons/build/Ionicons";
import "../styles/global.css";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(true);
  const [isFocused, setIsFocused] = useState(false);
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
      router.replace("/library");
    } catch (error: any) {
      Alert.alert(
        "Error",
        `Login failed: ${error?.message || "Unknown error"}`
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ScreenBackground>
      <View style={styles.container}>
        <Text style={styles.title}>Login</Text>

        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          placeholderTextColor="#aaa"
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <View style={styles.passwordContainer}>
          <TextInput
            style={[styles.passwordInput, isFocused && styles.inputFocused]}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Password"
            placeholderTextColor="#aaa"
            value={password}
            onChangeText={setPassword}
            secureTextEntry={passwordVisible}
          />
          <TouchableOpacity
            activeOpacity={0.7}
            onPress={() => setPasswordVisible((v) => !v)}
            accessibilityLabel={
              !passwordVisible ? "Hide password" : "Show password"
            }
          >
            <Ionicons
              name={passwordVisible ? "eye-off-outline" : "eye-outline"}
              size={24}
            />
          </TouchableOpacity>
        </View>

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

        <TouchableOpacity
          onPress={() => console.log("Forgot Password pressed")}
        >
          <Text style={styles.forgotPassword}>Forgot Password?</Text>
        </TouchableOpacity>
      </View>
    </ScreenBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 24,
    backgroundColor: "transparent",
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 32,
    color: "#fff",
    fontFamily: "Montserrat_700Bold",
  },
  input: {
    width: "100%",
    maxWidth: 340,
    height: 50,
    borderWidth: 1,
    borderColor: "#fff",
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 16,
    backgroundColor: "#fff",
    color: "#0A0414",
    fontFamily: "Montserrat_400Regular",
  },

  button: {
    width: "100%",
    maxWidth: 340,
    backgroundColor: "transparent",
    paddingVertical: 14,
    borderWidth: 1,
    borderColor: "#fff",
    borderRadius: 50,
    marginTop: 8,
    marginBottom: 16,
  },
  buttonText: {
    textAlign: "center",
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
    fontFamily: "Montserrat_700Bold",
  },
  forgotPassword: {
    color: "#ddd",
    fontSize: 14,
    fontFamily: "Montserrat_400Regular",
  },
  passwordContainer: {
    width: "100%",
    maxWidth: 340,
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#fff",
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 16,
    backgroundColor: "#fff",
    color: "#0A0414",
  },

  passwordInput: {
    flex: 1,
    backgroundColor: "transparent",
    height: 50,
    borderWidth: 0,
    padding: 0,
    fontFamily: "Montserrat_400Regular",
  },
  inputFocused: {
    borderWidth: 0,
    borderColor: "transparent",
  },
});
