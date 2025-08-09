import { Text, View, Image, StyleSheet, TouchableOpacity, Switch } from 'react-native'
import React, { useState } from 'react'
import { router } from 'expo-router';

export type ReadingSpeed = "slow" | "avarage" | "fast";
export default function Option() {
  const [developmentMode, setDevelopmentMode] = useState(true);
  const [readingSpeed, setReadingSpeed] = useState<ReadingSpeed>("slow");

  const handleBack = () => {
    const params = [];
    if (developmentMode) params.push("development=true");
    if (readingSpeed) params.push(`readingSpeed=${readingSpeed}`);
    const queryString = params.length ? `?${params.join("&")}` : "";
    router.push(queryString ? `/library${queryString}` as `/library?${string}` : "/library");
  }

  const ReadingSpeedButton = ({ speed, onPress }: { speed: ReadingSpeed, onPress: () => void }) => {
    return (
      <TouchableOpacity style={[styles.button, { backgroundColor: readingSpeed === speed ? "#FFD369" : "#5AD1B3" }]} onPress={() => {
        setReadingSpeed(speed);
        onPress();
      }}>
        <Text style={styles.h4}>{speed}</Text>
      </TouchableOpacity>
    )
  }

  return (
    <View>
      <TouchableOpacity
        style={styles.breadcrumbs}
        onPress={handleBack}
      >
        <Image source={require("../assets/images/chevron-left.svg")} />
        <Text style={styles.h2}>Go to Library</Text>
      </TouchableOpacity>
      <View style={[styles.optionsWrapper, { marginTop: 48, marginBottom: 32 }]}>
        <Text style={styles.h3}>Turn on Development mode</Text>
        <Switch value={developmentMode} onValueChange={setDevelopmentMode} />
      </View>
      <Text style={[styles.h3, { marginTop: 24, marginBottom: 12, textAlign: "center" }]}>
        Choose reading speed
      </Text>
      <View style={styles.buttonsWrapper}>
        <ReadingSpeedButton speed="slow" onPress={() => setReadingSpeed("slow")} />
        <ReadingSpeedButton speed="avarage" onPress={() => setReadingSpeed("avarage")} />
        <ReadingSpeedButton speed="fast" onPress={() => setReadingSpeed("fast")} />
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  h2: {
    fontFamily: "Montserrat_700Bold",
    fontWeight: "700",
    fontSize: 14,
    letterSpacing: 0,
    textAlign: "center",
    color: "white",
    marginLeft: "auto",
    marginRight: "auto",
  },
  h3: {
    fontFamily: "Montserrat_400Regular",
    fontWeight: "400",
    fontSize: 14,
    letterSpacing: 0,
    color: "white",
  },
  h4: {
    fontFamily: "Montserrat_400Regular",
    fontWeight: "400",
    fontSize: 14,
    letterSpacing: 0,
    textAlign: "center",
    color: "#0A0414",
  },
  breadcrumbs: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginLeft: 20,
    marginRight: 20,
    marginTop: 20,
    marginBottom: 20,
  },
  optionsWrapper: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginLeft: 20,
    marginRight: 20,
  },
  buttonsWrapper: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginLeft: 20,
    marginRight: 20,
  },
  button: {
    backgroundColor: "#5AD1B3",
    padding: 10,
    borderRadius: 19,
    flex: 1,
    height: 38,
    justifyContent: "center",
    alignItems: "center",
    marginHorizontal: 4,
  },
});
