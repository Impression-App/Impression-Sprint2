import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Alert, ToastAndroid } from "react-native";
import styles from "./ContactsStyle";
import ContactList from "../components/ContactList";
import { User } from "../helpers/interfaces";
import {
  getConnections,
  newGroup,
  getNearbyUsers,
  batchNewUsers,
  newConnection,
} from "../helpers/network";
import user from "../../config/user";
import { Button } from "react-native-paper";
import { createMaterialTopTabNavigator } from "@react-navigation/material-top-tabs";
import GroupsScreen from "./GroupScreen";
import FAB from "../components/FAB";
import { Entypo, Feather } from "@expo/vector-icons";
import * as Location from "expo-location";
import SelectionModal from "../components/SelectionModal";
import colors from "../../config/colors";
import font from "../../config/font";

function ContactsScreen({ navigation }: any) {
  const [userConnections, setUserConnections] = useState<User[]>([]);
  const [companyConnections, setCompanyConnections] = useState<User[]>([]);
  const [keyword, setKeyword] = useState("");
  const [isButtonVisible, setButtonVisible] = useState(false);
  const [selected, setSelected] = useState(new Set<number>());
  const [isSelection, setIsSelection] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);

  const makeListeners = () => {
    navigation.addListener("focus", () => {
      refreshData();
    });
  };

  const refreshData = () => {
    const parseConnections = (allConnections: User[]) => {
      setUserConnections(
        allConnections.filter(
          (connection) => connection.user_type === "Student"
        )
      );
      setCompanyConnections(
        allConnections.filter(
          (connection) => connection.user_type === "Recruiter"
        )
      );
    };

    getConnections(user.email)
      .then((response) => response.json())
      .then((data) => parseConnections(data["connections"]))
      .catch((err) => console.log(err));
  };
  useEffect(() => {
    refreshData();
    makeListeners();
  }, []);

  const createGroup = () => {
    const emails: string[] = [];
    const names: string[] = [];
    selected.forEach((i) => {
      emails.push(userConnections[i].email);
      names.push(userConnections[i].first_name);
    });
    emails.push(user.email);
    newGroup(names.join(", "), emails)
      .then((result) => result.json())
      .then((json) => {
        if (json["success"]) {
          ToastAndroid.show("Group created", ToastAndroid.LONG);
          resetList();
        } else {
          Alert.alert("Error", "There was an error with your request");
        }
      });
  };

  const resetList = () => {
    const temp = new Set<number>();
    setSelected(temp);
    setIsSelection(false);
  };
  const selectItem = () => {
    setModalVisible(true);
  };

  const selectionCallback = (email: string) => {
    setModalVisible(false);
    const newConnections: { user1_email: string, user2_email: string }[] = [];
    selected.forEach((i) => {
      newConnections.push({
        user1_email: email,
        user2_email: userConnections[i].email,
      });
    });
    resetList();
    batchNewUsers(newConnections)
      .then((response) => {
        if (response.ok) {
          ToastAndroid.show("Successfully shared Contacts", ToastAndroid.LONG);
        }
        return response.json();
      })
      .then((json) => {
        console.log(json);
      })
      .catch((err) => {
        ToastAndroid.show("Failed to share Contacts", ToastAndroid.LONG);
        console.log(err);
      });
  };

  const requestLocation = async () => {
    const { status } = await Location.requestPermissionsAsync();
    if (status !== "granted") {
      ToastAndroid.show(
        "Permission to access location was denied",
        ToastAndroid.LONG
      );
    }

    const location = await Location.getCurrentPositionAsync({});
    ToastAndroid.show("Fetchiing nearby users...", ToastAndroid.SHORT);

    getNearbyUsers(user.email, location.coords)
      .then((data) => data.json())
      .then(async (json) => {
        if (json["data"].length == 0) {
          ToastAndroid.show("No users nearby", ToastAndroid.LONG);
        } else {
          for (let i = 0; i < json.data.length; i++) {
            const person = json.data[i];
            await newConnection(person.email);
          }
          getConnections(user.email);
          ToastAndroid.show(
            "Users nearby have been added to your conenctions",
            ToastAndroid.LONG
          );
        }
      });
  };

  const updateKeyword = (value: string) => {
    setKeyword(value);
  };
  useEffect(() => {
    _handleSearch();
  }, [keyword]);

  const _handleSearch = () => {
    const userList = userConnections;
    const companyList = companyConnections;

    const kw = keyword.toLowerCase();
    const filteredUserList = userList.filter((item) => {
      if (item["first_name"].toLowerCase().includes(kw)) return item;
    });

    const filteredCompanyList = companyList.filter((item) => {
      if (item["first_name"].toLowerCase().includes(kw)) return item;
    });

    if (!keyword || keyword == "") {
      setUserConnections(userList);
      setCompanyConnections(companyList);
    } else {
      if (Array.isArray(filteredUserList)) {
        setUserConnections(filteredUserList);
      }
      if (Array.isArray(filteredCompanyList)) {
        setCompanyConnections(filteredCompanyList);
      }
    }
    if (keyword === "" || !keyword.trim().length) refreshData();
  };

  const emptyFunction = () => {}

  return (
    <View style={styles.container}>
      <View
        style={{
          width: "100%",
          marginTop: 0,
          justifyContent: "center",
          flexDirection: "row",
          alignItems: "center",
          paddingHorizontal: 16,
        }}
      >
        <Feather name="search" style={{ fontSize: 20 }} />
        <TextInput
          value={keyword}
          onChangeText={updateKeyword}
          style={{
            backgroundColor: colors.background,
            width: "95%",
            paddingHorizontal: 16,
            height: 50,
            color: colors.text,
            fontFamily: font.regular,
          }}
          placeholder="Search Contacts"
        />
      </View>
      {companyConnections.length > 0 && (
        <View style={{ flex: 2 }}>
          <Text style={styles.title}>Companies</Text>
          <ContactList
            contacts={companyConnections}
            setButtonVisible={emptyFunction}
            selected={new Set<number>()}
            setSelected={emptyFunction}
            isSelection={false}
            setIsSelection={emptyFunction}
          />
        </View>
      )}
      {userConnections.length > 0 && (
        <View style={{ flex: 2 }}>
          <Text style={styles.title}>Students</Text>
          <ContactList
            contacts={userConnections}
            setButtonVisible={setButtonVisible}
            selected={selected}
            setSelected={setSelected}
            isSelection={isSelection}
            setIsSelection={setIsSelection}
          />
        </View>
      )}
      <SelectionModal
        selectionCallback={selectionCallback}
        isVisible={modalVisible}
        setModalVisible={setModalVisible}
        people={userConnections}
      />

      {!companyConnections.length && !userConnections && (
        <Text style={styles.title}>
          You have no connections. Have someone scan your QR to create one
        </Text>
      )}
      {isButtonVisible ? (
        <Button onPress={createGroup}>Create Group</Button>
      ) : null}
      <FAB onPress={isSelection ? selectItem : requestLocation}>
        {isSelection ? (
          <Feather name="send" style={{ color: "white", fontSize: 35 }} />
        ) : (
          <Entypo name="map" style={{ color: "white", fontSize: 35 }} />
        )}
      </FAB>
    </View>
  );
}

const Tab = createMaterialTopTabNavigator();

export default function ContactScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Tab.Navigator>
        <Tab.Screen name="Contacts" component={ContactsScreen} />
        <Tab.Screen name="Groups" component={GroupsScreen} />
      </Tab.Navigator>
    </View>
  );
}
