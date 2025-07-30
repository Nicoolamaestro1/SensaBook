import { View, Text } from 'react-native'
import React from 'react'

export default function About() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#A02D1BFF" }}>
      <Text style={{ color: "white", fontSize: 32, fontWeight: "bold" }}>About</Text>
    </View>
  )
}