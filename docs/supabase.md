
  // User logic

  import { createClient } from "@supabase/supabase-js";

  const supabase = createClient(
  );

  async function signIn() {
    const user = await supabase.auth.getUser();
    console.log(user);
    console.log("user.data", user["data"]["user"]);

    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: "github",
    });
    console.log(data, error);
  }

  onMount(async () => {
    const user = await supabase.auth.getUser();
    console.log(user);
    console.log("user.data", user["data"]["user"]);
  });

  <button on:click={signIn}>Sign In</button>