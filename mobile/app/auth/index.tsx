import React, { useEffect, useRef } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
  Dimensions,
  Animated,
  Easing,
  ScrollView,
} from "react-native";
import { useRouter } from "expo-router";
import ScreenBackground from "../components/ScreenBackground";

const { width } = Dimensions.get("window");

export default function WelcomeScreen() {
  const router = useRouter();
  const logoOpacity = useRef(new Animated.Value(1)).current;
  const loginOpacity = useRef(new Animated.Value(0)).current;
  // --- letter-by-letter animation setup ---
  const word = "SensaBook";
  const letters = word.split("");
  const letterAnims = useRef(
    letters.map(() => ({
      opacity: new Animated.Value(0),
      translateY: new Animated.Value(16), // start slightly below
    }))
  ).current;

  useEffect(() => {
    const animations = letters.map((_, i) =>
      Animated.parallel([
        Animated.timing(letterAnims[i].opacity, {
          toValue: 1,
          duration: 300,
          delay: i * 70,
          easing: Easing.out(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(letterAnims[i].translateY, {
          toValue: 0,
          duration: 300,
          delay: i * 70,
          easing: Easing.out(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    );

    // run in sequence with a light stagger
    Animated.stagger(50, animations).start();
  }, [letterAnims, letters]);

  return (
    <ScreenBackground>
      <View style={styles.container}>
        <ScrollView
          contentContainerStyle={{ flexGrow: 1 }}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.logoHolder}>
            {/* Logo */}
            <Animated.Image
              source={require("../../assets/images/logo.png")}
              style={{
                width: 100,
                height: 100,
                opacity: logoOpacity,
                marginBottom: 5,
                shadowColor: "#C68A4B", // pick your glow color
                shadowOffset: { width: 0, height: 0 },
                shadowOpacity: 1,
                shadowRadius: 70,
                overflow: "visible",
              }}
              resizeMode="contain"
            />

            <View style={{ flexDirection: "row" }}>
              {/* Animated "SensaBook" */}
              {letters.map((ch, i) => (
                <Animated.Text
                  key={`${ch}-${i}`}
                  style={[
                    styles.logoTitle,
                    {
                      opacity: letterAnims[i].opacity,
                      transform: [{ translateY: letterAnims[i].translateY }],
                    },
                  ]}
                >
                  {ch}
                </Animated.Text>
              ))}
            </View>
            <Text style={styles.title}>
              Reading You
              {"\n"}
              Can Feel!
            </Text>
          </View>

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
              <Text style={styles.secondaryButtonText}>
                Continue with Google
              </Text>
            </TouchableOpacity>

            {/* Button - Apple */}
            <TouchableOpacity style={styles.secondaryButton}>
              <Image
                source={require("../../assets/images/apple.png")}
                style={styles.icon}
              />
              <Text style={styles.secondaryButtonText}>
                Continue with Apple
              </Text>
            </TouchableOpacity>

            {/* Button - Login */}
            <TouchableOpacity
              style={[styles.secondaryButton, styles.lastButton]}
              onPress={() => router.push("/auth/login")}
            >
              <Text style={styles.secondaryButtonText}>Log in</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </ScreenBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "space-between",
    paddingHorizontal: 24,
    fontFamily: "Montserrat_400Regular",
    paddingTop: 40,
    paddingBottom: 40,
    minHeight: "100%",
    overflow: "scroll",
    width: "100%",
    alignItems: "stretch",
  },

  logoHolder: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    marginTop: "30%",
  },

  logoTitle: {
    fontSize: 24,
    color: "#fff",
    fontFamily: "Montserrat_700Bold",
    textAlign: "center",
    marginBottom: 70,
  },

  icon: {
    width: 20,
    height: 20,
    position: "absolute",
    left: 15,
    top: 23,
    transform: [{ translateY: -10 }],
    resizeMode: "contain",
  },
  title: {
    fontFamily: "Montserrat_700Bold",
    fontSize: width * 0.09,
    textAlign: "center",
    marginBottom: 60,
    color: "#fff",
  },
  buttonGroup: {
    width: "100%",
    marginBottom: 40,
    alignSelf: "stretch",
  },
  primaryButton: {
    backgroundColor: "#fff",
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 32,
    marginBottom: 10,
    width: "100%",
    alignSelf: "stretch",
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
    alignSelf: "stretch",
  },
  secondaryButtonText: {
    color: "#fff",
    fontSize: 16,
    textAlign: "center",
    fontFamily: "Montserrat_700Bold",
  },
  lastButton: {
    marginTop: 40,
  },
});
