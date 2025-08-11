import React, { useEffect, useRef, useState } from "react";
import { View, Animated, Text, Easing } from "react-native";
import WelcomeScreen from "./auth/index";
import ScreenBackground from "./components/ScreenBackground";

export default function Index() {
  const logoOpacity = useRef(new Animated.Value(1)).current;
  const loginOpacity = useRef(new Animated.Value(0)).current;
  const [showLogin, setShowLogin] = useState(false);

  const letters = "SensaBook".split("");
  const letterAnimations = useRef(
    letters.map(() => ({
      opacity: new Animated.Value(0),
      translateY: new Animated.Value(20),
    }))
  ).current;

  useEffect(() => {
    // Animate letters after short delay
    const animateLetters = () => {
      const animations = letters.map((_, i) =>
        Animated.parallel([
          Animated.timing(letterAnimations[i].opacity, {
            toValue: 1,
            duration: 300,
            delay: i * 80, // stagger each letter
            easing: Easing.out(Easing.ease),
            useNativeDriver: true,
          }),
          Animated.timing(letterAnimations[i].translateY, {
            toValue: 0,
            duration: 300,
            delay: i * 80,
            easing: Easing.out(Easing.ease),
            useNativeDriver: true,
          }),
        ])
      );
      Animated.stagger(50, animations).start(() => {
        // Wait 1s after letters finish, fade out, then show login
        setTimeout(() => {
          Animated.timing(logoOpacity, {
            toValue: 0,
            duration: 500,
            useNativeDriver: true,
          }).start(() => {
            setShowLogin(true);
            Animated.timing(loginOpacity, {
              toValue: 1,
              duration: 800,
              useNativeDriver: true,
            }).start();
          });
        }, 1000);
      });
    };

    animateLetters();
  }, []);

  return (
    <ScreenBackground>
      <View
        style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {!showLogin && (
          <>
            {/* Logo */}
            <Animated.Image
              source={require("../assets/images/logo.png")}
              style={{
                width: 120,
                height: 120,
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

            {/* Animated text */}
            <View style={{ flexDirection: "row" }}>
              {letters.map((letter, i) => (
                <Animated.Text
                  key={i}
                  style={{
                    fontSize: 24,
                    color: "#fff",
                    fontFamily: "Montserrat_700Bold",
                    opacity: letterAnimations[i].opacity,

                    transform: [{ translateY: letterAnimations[i].translateY }],
                  }}
                >
                  {letter}
                </Animated.Text>
              ))}
            </View>
          </>
        )}

        {showLogin && (
          <Animated.View
            style={{ flex: 1, width: "100%", opacity: loginOpacity }}
          >
            <WelcomeScreen />
          </Animated.View>
        )}
      </View>
    </ScreenBackground>
  );
}
