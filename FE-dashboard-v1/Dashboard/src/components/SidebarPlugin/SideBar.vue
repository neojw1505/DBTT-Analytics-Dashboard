<template>
  <div class="sidebar" :data="backgroundColor">
    <!--
            Tip 1: you can change the color of the sidebar's background using: data-background-color="white | black | darkblue"
            Tip 2: you can change the color of the active button using the data-active-color="primary | info | success | warning | danger"
        -->
    <!-- -->
    <div class="sidebar-wrapper" id="style-3">
      <div class="logo">
        <a
          href="http://www.creative-tim.com"
          aria-label="sidebar mini logo"
          class="simple-text logo-mini"
        >
          <div class="logo-img" :class="{ 'logo-img-rtl': $rtl.isRTL }">
            <img
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAV1BMVEVHcEwoAIgoAIgoAIgoAIgpAIgoAIgpAIgoAIgoAIcoAIgoAIgoAIggAIUUAIIEAH9bS552aawAAHwoAIerpMv////u7PW7tdTNyN/b2OmDd7OUi71DK5NLLFmyAAAAFHRSTlMAM4fC7P/DYWAX4D//////////M6cOrdYAAAEpSURBVHgBXZMFEoQwDEWLBE0Nt/ufc38zmUUe2r5KMgTzJ8uLkqis8sx8qUv6UzYv1Xb0omtv1xPLgRNwuvrbPWES1LasvW/diuw+s1j3NaAhwQKmJzUkcmB2PsQYaHD23qM0ZkxvbpqFZY3OO+ADbGZySLfN+xHjuc1gX89zWk5LlJsqyXU+vbOYFNdlThwe3QW2BD4EvoiJrfM2hMtbAqXRWN0xrw7S4pKwGZdKgpwccwiWbmRZJr72eQlumNYBlllzKXRmnKfhmAHiVCpJhYlsWtZFOC8rEchNJo6RzcVu2jeEBUSORje1EYHa4P0dUZkKRJORKJglDTma9yd70ZlEqwHoxZpK+y6TF3cRsfZoDnw7Kc27/12aQvMs6tp8GfOqhCgev8MPP8wXTFX3hpEAAAAASUVORK5CYII="
            />
          </div>
        </a>
        <a href="http://www.creative-tim.com" class="simple-text logo-normal">
          I <i class="tim-icons icon-heart-2"></i> DBTT
        </a>
      </div>
      <slot> </slot>
      <ul class="nav">
        <!--By default vue-router adds an active class to each route link. This way the links are colored when clicked-->
        <slot name="links">
          <sidebar-link
            v-for="(link, index) in sidebarLinks"
            :key="index"
            :to="link.path"
            :name="link.name"
            :icon="link.icon"
          >
          </sidebar-link>
        </slot>
      </ul>
    </div>
  </div>
</template>
<script>
import SidebarLink from "./SidebarLink";

export default {
  props: {
    title: {
      type: String,
      default: "I LOVE DBTT",
    },
    backgroundColor: {
      type: String,
      default: "vue",
    },
    activeColor: {
      type: String,
      default: "success",
      validator: (value) => {
        let acceptedValues = [
          "primary",
          "info",
          "success",
          "warning",
          "danger",
        ];
        return acceptedValues.indexOf(value) !== -1;
      },
    },
    sidebarLinks: {
      type: Array,
      default: () => [],
    },
    autoClose: {
      type: Boolean,
      default: true,
    },
  },
  provide() {
    return {
      autoClose: this.autoClose,
      addLink: this.addLink,
      removeLink: this.removeLink,
    };
  },
  components: {
    SidebarLink,
  },
  computed: {
    /**
     * Styles to animate the arrow near the current active sidebar link
     * @returns {{transform: string}}
     */
    arrowMovePx() {
      return this.linkHeight * this.activeLinkIndex;
    },
    shortTitle() {
      return this.title
        .split(" ")
        .map((word) => word.charAt(0))
        .join("")
        .toUpperCase();
    },
  },
  data() {
    return {
      linkHeight: 65,
      activeLinkIndex: 0,
      windowWidth: 0,
      isWindows: false,
      hasAutoHeight: false,
      links: [],
    };
  },
  methods: {
    findActiveLink() {
      this.links.forEach((link, index) => {
        if (link.isActive()) {
          this.activeLinkIndex = index;
        }
      });
    },
    addLink(link) {
      const index = this.$slots.links.indexOf(link.$vnode);
      this.links.splice(index, 0, link);
    },
    removeLink(link) {
      const index = this.links.indexOf(link);
      if (index > -1) {
        this.links.splice(index, 1);
      }
    },
  },
  mounted() {
    this.$watch("$route", this.findActiveLink, {
      immediate: true,
    });
  },
};
</script>
