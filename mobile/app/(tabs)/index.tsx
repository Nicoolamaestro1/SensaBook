import React, { useEffect, useRef, useState } from "react";
import { View, Animated } from "react-native";
import LoginScreen from "../login";

export default function Index() {
  const logoOpacity = useRef(new Animated.Value(1)).current;   // animacija loga
  const loginOpacity = useRef(new Animated.Value(0)).current;  // animacija login-a
  const [showLogin, setShowLogin] = useState(false);

  useEffect(() => {
    // posle 2 sekunde animiraj logo da nestane
    const timer = setTimeout(() => {
      Animated.timing(logoOpacity, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }).start(() => {
        // kad logo nestane → prikaži login i animiraj ga
        setShowLogin(true);
        Animated.timing(loginOpacity, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }).start();
      });
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Logo animacija */}
      {!showLogin && (
        <Animated.Image
          source={require("../../assets/images/logo.png")} // 👈 pazi na putanju
          style={{
            width: 120,
            height: 120,
            opacity: logoOpacity,
            
          }}
          resizeMode="contain"
        />
      )}

      {/* Login animacija */}
      {showLogin && (
        <Animated.View style={{ flex: 1, width: "100%", opacity: loginOpacity }}>
          <LoginScreen />
        </Animated.View>
      )}
    </View>
  );
}
