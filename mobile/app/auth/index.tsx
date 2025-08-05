import { View, Text, TouchableOpacity, StyleSheet, Image, Dimensions } from "react-native";
import { useRouter } from "expo-router";
const { width } = Dimensions.get("window");

export default function WelcomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      {/* Logo */}
      <Image
          source={require("../../assets/images/logo.png")}
          style={styles.logo} />


      <Text style={styles.title}>Reading You Can Feel!</Text>
      <View style={styles.buttonGroup}>
        {/* Button - Sign up */}
        <TouchableOpacity style={styles.primaryButton}>
          <Text style={styles.primaryButtonText}>Sign up</Text>
        </TouchableOpacity>

        {/* Button - Google */}
        <TouchableOpacity style={styles.secondaryButton}>
          <Image
            source={require("../../assets/images/google.png")}
            style={styles.icon}
          />
          <Text style={styles.secondaryButtonText}>Continue with Google</Text>
        </TouchableOpacity>

        {/* Button - Apple */}
        <TouchableOpacity style={styles.secondaryButton}>
          <Image
            source={require("../../assets/images/apple.png")}
            style={styles.icon}
          />
          <Text style={styles.secondaryButtonText}>Continue with Apple</Text>
        </TouchableOpacity>

        {/* Button - Login */}
        <TouchableOpacity
          style={[styles.secondaryButton, styles.lastButton]}
          onPress={() => router.push("/auth/login")}
        >
          <Text style={styles.secondaryButtonText}>Log in</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 24,
    fontFamily: "Montserrat_400Regular",
  },
  logo: {
    marginTop: "40%",
    marginBottom: 40,
    width: 120,
    height: 120,
          
  },
  icon: {
    width: 20,
    height: 20,
    marginRight: 12,
    resizeMode: "contain",
    position: "absolute",
    left: 15,
    top: "50%",
    transform: "translateY(-50%)"
  },
  title: {
    fontFamily: "Montserrat_700Bold",
    fontSize: width * 0.11,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 40,
    color: "#fff",
  },
  buttonGroup: {
    width: "100%",
    marginBottom: 40,
  },
  primaryButton: {
    backgroundColor: "#FF3586",
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 32,
    marginBottom: 10,
    width: "100%",
  },
  primaryButtonText: {
    color: "#000",
    fontSize: 16,
    textAlign: "center",
    fontFamily: "Montserrat_700Bold",
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: "#fff",
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 32,
    marginBottom: 10,
    width: "100%",
  },
  secondaryButtonText: {
    color: "#fff",
    fontSize: 16,
    textAlign: "center",
    fontFamily: "Montserrat_700Bold",

  },
  lastButton: {
    marginTop: 40
  }
});
