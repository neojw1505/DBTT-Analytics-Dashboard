<template>
  <footer class="footer">
    <div class="container-fluid">
      <div class="copyright">
        © {{ year }} made by
        <a href="https://www.linkedin.com/in/neo-j-53b14624b/" target="_blank" rel="noopener"
          >Neo Jun Wei</a
        >&nbsp;&
        <a href="https://www.linkedin.com/in/yan-teng-hon-zavier/" target="_blank" rel="noopener"
          >Zavier Yan</a
        >
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      year: new Date().getFullYear(),
    };
  },
};
</script>
<style></style>
