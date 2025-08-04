import React, { useEffect, useRef, useState } from "react";
import { View, Animated } from "react-native";
import LoginScreen from "../login";

export default function Index() {
  const logoOpacity = useRef(new Animated.Value(1)).current;   
  const loginOpacity = useRef(new Animated.Value(0)).current; 
  const [showLogin, setShowLogin] = useState(false);

  useEffect(() => {
    // fake loading for 2 seconds
    const timer = setTimeout(() => {
      Animated.timing(logoOpacity, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }).start(() => {
        // show login after logo's gone
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
      {/* Logo animation */}
      {!showLogin && (
        <Animated.Image
          source={require("../../assets/images/logo.png")} 
          style={{
            width: 120,
            height: 120,
            opacity: logoOpacity,
            
          }}
          resizeMode="contain"
        />
      )}

      {/* Login animation */}
      {showLogin && (
        <Animated.View style={{ flex: 1, width: "100%", opacity: loginOpacity }}>
          <LoginScreen />
        </Animated.View>
      )}
    </View>
  );
}
